import { PrismaClient } from "@prisma/client";
import { Request, Response, Router } from "express";
import {
  createTaskRequestModel,
  CreateTaskRequest,
  updateTaskRequestModel,
  UpdateTaskRequest,
} from "../models/task.model";
import { validateRequest } from "../models/request-validation";

export type TaskDatabase = Pick<PrismaClient, "task">;

export function createTasksRouter(prisma: TaskDatabase) {
  const router = Router();

  router.get("/", async (_req: Request, res: Response) => {
    const tasks = await prisma.task.findMany({
      orderBy: { createdAt: "desc" },
    });
    res.json(tasks);
  });

  router.post(
    "/",
    validateRequest(createTaskRequestModel),
    async (_req: Request, res: Response) => {
      const request = res.locals.requestModel as CreateTaskRequest;
      const task = await prisma.task.create({ data: request });
      res.status(201).json(task);
    },
  );

  router.patch(
    "/:id",
    validateRequest(updateTaskRequestModel),
    async (_req: Request, res: Response) => {
      const request = res.locals.requestModel as UpdateTaskRequest;

      try {
        const task = await prisma.task.update({
          where: { id: request.id },
          data: { done: request.done },
        });
        res.json(task);
      } catch {
        res.status(404).json({ error: "Task not found" });
      }
    },
  );

  return router;
}
