require("dotenv").config();
const express = require("express");
const cors = require("cors");
const routes = require("./routes");
const { connectToMongo } = require("./config/mongo");
const { pool } = require("./config/postgres");

const app = express();

app.use(
  cors({
    origin: process.env.CORS_ORIGIN || "http://localhost:5173",
  }),
);
app.use(express.json());

app.get("/health", async (_req, res) => {
  try {
    await pool.query("SELECT 1");
    return res.json({ status: "ok", service: "study-hub-backend" });
  } catch (error) {
    return res.status(500).json({ status: "error", details: error.message });
  }
});

app.use("/api", routes);

app.use((error, _req, res, _next) => {
  console.error(error);
  res.status(500).json({ message: "Unexpected server error." });
});

const port = Number(process.env.PORT || 4000);

connectToMongo().finally(() => {
  app.listen(port, () => {
    console.log(`Study Hub backend running on port ${port}`);
  });
});
