import type { Request } from "express";

export type ValidationResult<T> =
  | { valid: true; value: T }
  | { valid: false; error: string };

export interface CreateTaskRequest {
  title: string;
}

export interface UpdateTaskRequest {
  id: number;
  done: boolean;
}

export function createTaskRequestModel(
  request: Pick<Request, "body">,
): ValidationResult<CreateTaskRequest> {
  if (
    !request.body ||
    typeof request.body !== "object" ||
    !("title" in request.body)
  ) {
    return { valid: false, error: "Title is required" };
  }

  const title = (request.body as { title?: unknown }).title;
  if (typeof title !== "string" || title.trim().length === 0) {
    return { valid: false, error: "Title is required" };
  }

  return { valid: true, value: { title: title.trim() } };
}

export function updateTaskRequestModel(
  request: Pick<Request, "params" | "body">,
): ValidationResult<UpdateTaskRequest> {
  const id = Number(request.params.id);
  const done = request.body?.done;

  if (!Number.isInteger(id) || typeof done !== "boolean") {
    return {
      valid: false,
      error: "A numeric id and boolean done value are required",
    };
  }

  return { valid: true, value: { id, done } };
}
