const express = require("express");
const authRoutes = require("./authRoutes");
const preferencesRoutes = require("./preferencesRoutes");
const placesRoutes = require("./placesRoutes");
const reviewsRoutes = require("./reviewsRoutes");

const router = express.Router();

router.use("/auth", authRoutes);
router.use("/preferences", preferencesRoutes);
router.use("/places", placesRoutes);
router.use("/places", reviewsRoutes);

module.exports = router;
