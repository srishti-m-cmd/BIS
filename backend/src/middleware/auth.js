const jwt = require("jsonwebtoken");

function authMiddleware(req, res, next) {
  const authHeader = req.headers.authorization;

  if (!authHeader || !authHeader.startsWith("Bearer ")) {
    return res.status(401).json({ message: "Missing or invalid token." });
  }

  const token = authHeader.split(" ")[1];
  const secret = process.env.JWT_SECRET;

  if (!secret) {
    return res.status(500).json({ message: "JWT_SECRET is not configured." });
  }

  try {
    const payload = jwt.verify(token, secret);
    req.user = { email: payload.email, name: payload.name };
    return next();
  } catch (error) {
    return res.status(401).json({ message: "Token verification failed." });
  }
}

module.exports = { authMiddleware };
