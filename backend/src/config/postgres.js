const { Pool } = require("pg");

const connectionString =
  process.env.POSTGRES_URL ||
  "postgresql://postgres:postgres@localhost:5432/studyhub";

const pool = new Pool({ connectionString });

pool.on("error", (error) => {
  console.error("PostgreSQL pool error:", error.message);
});

module.exports = { pool };
