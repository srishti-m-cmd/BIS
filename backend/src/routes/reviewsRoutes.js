const express = require("express");
const { getReviews, addReview } = require("../controllers/reviewsController");
const { authMiddleware } = require("../middleware/auth");

const router = express.Router();

router.get("/:placeId/reviews", authMiddleware, getReviews);
router.post("/:placeId/reviews", authMiddleware, addReview);

module.exports = router;
