const { pool } = require("../config/postgres");

async function getPreferences(req, res) {
  try {
    const result = await pool.query(
      "SELECT email, wifi, indoor, outdoor FROM preferences WHERE email = $1",
      [req.user.email],
    );

    if (result.rowCount === 0) {
      return res.json({
        email: req.user.email,
        wifi: false,
        indoor: false,
        outdoor: false,
      });
    }

    return res.json(result.rows[0]);
  } catch (error) {
    return res.status(500).json({ message: "Failed to fetch preferences.", error: error.message });
  }
}

async function upsertPreferences(req, res) {
  const { wifi = false, indoor = false, outdoor = false } = req.body;

  try {
    const result = await pool.query(
      `INSERT INTO preferences(email, wifi, indoor, outdoor)
       VALUES($1, $2, $3, $4)
       ON CONFLICT (email) DO UPDATE
       SET wifi = EXCLUDED.wifi,
           indoor = EXCLUDED.indoor,
           outdoor = EXCLUDED.outdoor
       RETURNING email, wifi, indoor, outdoor`,
      [req.user.email, wifi, indoor, outdoor],
    );

    return res.json(result.rows[0]);
  } catch (error) {
    return res.status(500).json({ message: "Failed to save preferences.", error: error.message });
  }
}

module.exports = { getPreferences, upsertPreferences };
