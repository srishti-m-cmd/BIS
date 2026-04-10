require("dotenv").config({ path: `${__dirname}/../.env` });
const fs = require("fs");
const path = require("path");
const { pool } = require("../src/config/postgres");

async function seedDb() {
  const sqlPath = path.join(__dirname, "../sql/seed.sql");
  const sql = fs.readFileSync(sqlPath, "utf8");

  try {
    await pool.query(sql);
    console.log("Mock place data seeded successfully.");
  } catch (error) {
    console.error("Seeding failed:", error.message);
    process.exitCode = 1;
  } finally {
    await pool.end();
  }
}

seedDb();
