require("dotenv").config({ path: `${__dirname}/../.env` });
const fs = require("fs");
const path = require("path");
const { pool } = require("../src/config/postgres");

async function initDb() {
  const sqlPath = path.join(__dirname, "../sql/init.sql");
  const sql = fs.readFileSync(sqlPath, "utf8");

  try {
    await pool.query(sql);
    console.log("Database schema initialized successfully.");
  } catch (error) {
    console.error("Database initialization failed:", error.message);
    process.exitCode = 1;
  } finally {
    await pool.end();
  }
}

initDb();
