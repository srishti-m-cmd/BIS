const express = require("express");
const { getPreferences, upsertPreferences } = require("../controllers/preferencesController");
const { authMiddleware } = require("../middleware/auth");

const router = express.Router();

router.get("/", authMiddleware, getPreferences);
router.put("/", authMiddleware, upsertPreferences);

module.exports = router;
