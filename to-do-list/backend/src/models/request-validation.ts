import { NextFunction, Request, RequestHandler, Response } from "express";
import { ValidationResult } from "./task.model";

export type RequestModel<T> = (request: Request) => ValidationResult<T>;

export function validateRequest<T>(model: RequestModel<T>): RequestHandler {
  return (request: Request, response: Response, next: NextFunction) => {
    const result = model(request);
    if (!result.valid) {
      response.status(400).json({ error: result.error });
      return;
    }

    response.locals.requestModel = result.value;
    next();
  };
}
