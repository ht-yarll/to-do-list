import { beforeEach, describe, expect, it, vi } from "vitest";
import request from "supertest";
import { createApp, TaskDatabase } from "../../to-do-list/backend/src/app";

const task = {
  id: 1,
  title: "Buy milk",
  done: false,
  createdAt: new Date("2026-01-01"),
};

function createDatabaseMock() {
  return {
    task: {
      findMany: vi.fn(),
      create: vi.fn(),
      update: vi.fn(),
    },
  } as unknown as TaskDatabase;
}

describe("task HTTP API", () => {
  let database: TaskDatabase;

  beforeEach(() => {
    database = createDatabaseMock();
  });

  it("lists tasks newest first", async () => {
    vi.mocked(database.task.findMany).mockResolvedValue([task]);

    const response = await request(createApp(database)).get("/tasks");

    expect(response.status).toBe(200);
    expect(response.body).toEqual([
      { ...task, createdAt: task.createdAt.toISOString() },
    ]);
    expect(database.task.findMany).toHaveBeenCalledWith({
      orderBy: { createdAt: "desc" },
    });
  });

  it("creates a task from a valid request", async () => {
    vi.mocked(database.task.create).mockResolvedValue(task);

    const response = await request(createApp(database))
      .post("/tasks")
      .send({ title: "  Buy milk  " });

    expect(response.status).toBe(201);
    expect(response.body).toEqual({
      ...task,
      createdAt: task.createdAt.toISOString(),
    });
    expect(database.task.create).toHaveBeenCalledWith({
      data: { title: "Buy milk" },
    });
  });

  it("rejects an invalid create request", async () => {
    const response = await request(createApp(database))
      .post("/tasks")
      .send({ title: "" });

    expect(response.status).toBe(400);
    expect(response.body).toEqual({ error: "Title is required" });
    expect(database.task.create).not.toHaveBeenCalled();
  });

  it("updates a task using a numeric id", async () => {
    vi.mocked(database.task.update).mockResolvedValue({ ...task, done: true });

    const response = await request(createApp(database))
      .patch("/tasks/1")
      .send({ done: true });

    expect(response.status).toBe(200);
    expect(response.body.done).toBe(true);
    expect(database.task.update).toHaveBeenCalledWith({
      where: { id: 1 },
      data: { done: true },
    });
  });

  it("rejects an invalid update request", async () => {
    const response = await request(createApp(database))
      .patch("/tasks/not-a-number")
      .send({ done: "yes" });

    expect(response.status).toBe(400);
    expect(database.task.update).not.toHaveBeenCalled();
  });

  it("returns 404 when the database cannot find a task", async () => {
    vi.mocked(database.task.update).mockRejectedValue(new Error("not found"));

    const response = await request(createApp(database))
      .patch("/tasks/1")
      .send({ done: true });

    expect(response.status).toBe(404);
    expect(response.body).toEqual({ error: "Task not found" });
  });
});
