const bcrypt = require("bcryptjs");
const jwt = require("jsonwebtoken");
const { pool } = require("../config/postgres");

function createToken(user) {
  return jwt.sign(
    { email: user.email, name: user.name },
    process.env.JWT_SECRET,
    { expiresIn: process.env.JWT_EXPIRES_IN || "7d" },
  );
}

async function signup(req, res) {
  const { name, email, password, wifi = false, indoor = false, outdoor = false } =
    req.body;

  if (!name || !email || !password) {
    return res.status(400).json({ message: "name, email, and password are required." });
  }

  try {
    const existing = await pool.query("SELECT email FROM users WHERE email = $1", [email]);
    if (existing.rowCount > 0) {
      return res.status(409).json({ message: "Email already registered." });
    }

    const passwordHash = await bcrypt.hash(password, 10);
    await pool.query(
      "INSERT INTO users(email, name, password) VALUES($1, $2, $3)",
      [email, name, passwordHash],
    );

    await pool.query(
      `INSERT INTO preferences(email, wifi, indoor, outdoor)
       VALUES($1, $2, $3, $4)
       ON CONFLICT (email) DO UPDATE
       SET wifi = EXCLUDED.wifi,
           indoor = EXCLUDED.indoor,
           outdoor = EXCLUDED.outdoor`,
      [email, wifi, indoor, outdoor],
    );

    const token = createToken({ email, name });
    return res.status(201).json({ token, user: { email, name } });
  } catch (error) {
    return res.status(500).json({ message: "Signup failed.", error: error.message });
  }
}

async function login(req, res) {
  const { username, email, password } = req.body;
  const identity = email || username;

  if (!identity || !password) {
    return res.status(400).json({ message: "username/email and password are required." });
  }

  try {
    const userResult = await pool.query(
      `SELECT email, name, password
       FROM users
       WHERE email = $1 OR lower(name) = lower($1)
       LIMIT 1`,
      [identity],
    );

    if (userResult.rowCount === 0) {
      return res.status(401).json({ message: "Invalid credentials." });
    }

    const user = userResult.rows[0];
    const valid = await bcrypt.compare(password, user.password);

    if (!valid) {
      return res.status(401).json({ message: "Invalid credentials." });
    }

    const token = createToken(user);
    return res.json({ token, user: { email: user.email, name: user.name } });
  } catch (error) {
    return res.status(500).json({ message: "Login failed.", error: error.message });
  }
}

module.exports = { signup, login };
