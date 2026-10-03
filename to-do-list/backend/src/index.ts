import { PrismaClient } from "@prisma/client";
import { createApp } from "./app";

const prisma = new PrismaClient();
const app = createApp(prisma);

// Start the server
const PORT = Number(process.env.PORT ?? 3000);
app.listen(PORT, () => {
  console.log(`Backend server running on http://localhost:${PORT}`);
});
