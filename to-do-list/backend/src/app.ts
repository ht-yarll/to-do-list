import "dotenv/config";
import cors from "cors";
import express, { Request, Response } from "express";
import { createTasksRouter, TaskDatabase } from "./routes/tasks.routes";

export type { TaskDatabase } from "./routes/tasks.routes";

function getAllowedOrigins() {
  const configuredOrigins = process.env.CORS_ALLOWED_ORIGINS?.split(",")
    .map((origin) => origin.trim())
    .filter(Boolean);

  if (configuredOrigins?.length) {
    return configuredOrigins;
  }

  if (process.env.NODE_ENV === "production") {
    throw new Error("CORS_ALLOWED_ORIGINS must be set in production");
  }

  return ["http://localhost:5173"];
}

export function createApp(prisma: TaskDatabase) {
  const app = express();

  app.use(cors({ origin: getAllowedOrigins() }));
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
