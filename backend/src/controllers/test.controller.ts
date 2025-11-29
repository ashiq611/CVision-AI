import { Request, Response } from "express";

export const testController = async (req: Request, res: Response) => {
  res.json({
    status: "ok",
    message: "Backend is running..."
  });
};
