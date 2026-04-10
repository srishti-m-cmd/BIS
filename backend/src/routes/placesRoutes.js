const express = require("express");
const {
  getRecommendations,
  getPlaceById,
  getMongoNearby,
} = require("../controllers/placesController");
const { authMiddleware } = require("../middleware/auth");

const router = express.Router();

router.get("/recommendations", authMiddleware, getRecommendations);
router.get("/mongo-near", authMiddleware, getMongoNearby);
router.get("/:placeId", authMiddleware, getPlaceById);

module.exports = router;
