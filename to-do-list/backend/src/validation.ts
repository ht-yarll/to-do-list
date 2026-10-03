import type { Request } from "express";
import {
  createTaskRequestModel,
  updateTaskRequestModel,
  ValidationResult,
} from "./models/task.model";

export type { ValidationResult } from "./models/task.model";

export function validateCreateTask(
  input: unknown,
): ValidationResult<{ title: string }> {
  return createTaskRequestModel({ body: input });
}

export function validateTaskUpdate(
  rawId: string,
  done: unknown,
): ValidationResult<{ id: number; done: boolean }> {
  return updateTaskRequestModel({
    params: { id: rawId },
    body: { done },
  } as Pick<Request, "params" | "body">);
}
