import { PrismaClient } from "@prisma/client";
import cors from "cors";
import express, { Request, Response } from "express";
import { validateCreateTask, validateTaskUpdate } from "./validation";

export type TaskDatabase = Pick<PrismaClient, "task">;

export function createApp(prisma: TaskDatabase) {
  const app = express();

  app.use(cors());
  app.use(express.json());

  app.get("/health", (_req: Request, res: Response) => {
    res.status(200).json({ status: "ok" });
  });

  app.get("/tasks", async (_req: Request, res: Response) => {
    const tasks = await prisma.task.findMany({
      orderBy: { createdAt: "desc" },
    });
    res.json(tasks);
  });

  app.post("/tasks", async (req: Request, res: Response) => {
    const result = validateCreateTask(req.body);
    if (!result.valid) {
      return res.status(400).json({ error: result.error });
    }

    const task = await prisma.task.create({ data: result.value });
    res.status(201).json(task);
  });

  app.patch("/tasks/:id", async (req: Request, res: Response) => {
    const rawId = typeof req.params.id === "string" ? req.params.id : "";
    const result = validateTaskUpdate(rawId, req.body?.done);
    if (!result.valid) {
      return res.status(400).json({ error: result.error });
    }

    try {
      const task = await prisma.task.update({
        where: { id: result.value.id },
        data: { done: result.value.done },
      });
      res.json(task);
    } catch {
      res.status(404).json({ error: "Task not found" });
    }
  });

  return app;
}
