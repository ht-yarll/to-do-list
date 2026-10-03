import { describe, expect, it } from "vitest";
import {
  createTaskRequestModel,
  updateTaskRequestModel,
} from "../../to-do-list/backend/src/models/task.model";

describe("task validation", () => {
  it("accepts and trims a non-empty title", () => {
    expect(createTaskRequestModel({ body: { title: "  Buy milk  " } })).toEqual(
      {
        valid: true,
        value: { title: "Buy milk" },
      },
    );
  });

  it("rejects missing, empty, and non-string titles", () => {
    expect(createTaskRequestModel({ body: {} })).toEqual({
      valid: false,
      error: "Title is required",
    });
    expect(createTaskRequestModel({ body: { title: "   " } })).toEqual({
      valid: false,
      error: "Title is required",
    });
    expect(createTaskRequestModel({ body: { title: 123 } })).toEqual({
      valid: false,
      error: "Title is required",
    });
  });

  it("accepts numeric ids and boolean completion values", () => {
    expect(
      updateTaskRequestModel({ params: { id: "7" }, body: { done: true } }),
    ).toEqual({
      valid: true,
      value: { id: 7, done: true },
    });
  });

  it("rejects invalid ids and completion values", () => {
    expect(
      updateTaskRequestModel({ params: { id: "abc" }, body: { done: true } })
        .valid,
    ).toBe(false);
    expect(
      updateTaskRequestModel({ params: { id: "7" }, body: { done: "true" } })
        .valid,
    ).toBe(false);
  });
});
