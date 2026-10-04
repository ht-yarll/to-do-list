import cors from "cors";
import express, { Request, Response } from "express";
import { createTasksRouter, TaskDatabase } from "./routes/tasks.routes";

export type { TaskDatabase } from "./routes/tasks.routes";

export function createApp(prisma: TaskDatabase) {
  const app = express();

  app.use(cors());
  app.use(express.json());

  app.get("/health", async (_req: Request, res: Response) => {
    try {
      await prisma.$queryRaw`SELECT 1`;
      res.status(200).json({ status: "ok" });
    } catch {
      res.status(503).json({ status: "unhealthy" });
    }
  });

  app.use("/tasks", createTasksRouter(prisma));

  return app;
}
