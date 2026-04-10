const PlaceGeo = require("../models/PlaceGeo");
const { pool } = require("../config/postgres");

async function syncPlaceRatingInMongo(placeId) {
  const placeResult = await pool.query(
    `SELECT p.place_id, p.rating, COUNT(r.place_id)::int AS review_count
     FROM places p
     LEFT JOIN reviews r ON p.place_id = r.place_id
     WHERE p.place_id = $1
     GROUP BY p.place_id`,
    [placeId],
  );

  if (placeResult.rowCount === 0) {
    return;
  }

  const updated = placeResult.rows[0];
  await PlaceGeo.findOneAndUpdate(
    { placeId: Number(placeId) },
    { rating: Number(updated.rating || 0), reviewCount: Number(updated.review_count || 0) },
    { new: true },
  );
}

async function getReviews(req, res) {
  const placeId = Number(req.params.placeId);
  if (!Number.isInteger(placeId)) {
    return res.status(400).json({ message: "Invalid place id." });
  }

  try {
    const placeResult = await pool.query(
      "SELECT place_id, name, rating FROM places WHERE place_id = $1",
      [placeId],
    );

    if (placeResult.rowCount === 0) {
      return res.status(404).json({ message: "Place not found." });
    }

    const reviewsResult = await pool.query(
      `SELECT email, rating, comment, created_at
       FROM reviews
       WHERE place_id = $1
       ORDER BY created_at DESC`,
      [placeId],
    );

    return res.json({
      place: placeResult.rows[0],
      reviews: reviewsResult.rows,
    });
  } catch (error) {
    return res.status(500).json({ message: "Failed to fetch reviews.", error: error.message });
  }
}

async function addReview(req, res) {
  const placeId = Number(req.params.placeId);
  const rating = Number(req.body.rating);
  const comment = (req.body.comment || "").trim();

  if (!Number.isInteger(placeId)) {
    return res.status(400).json({ message: "Invalid place id." });
  }

  if (!Number.isFinite(rating) || rating < 1 || rating > 5) {
    return res.status(400).json({ message: "Rating must be between 1 and 5." });
  }

  try {
    const placeExists = await pool.query("SELECT place_id FROM places WHERE place_id = $1", [placeId]);
    if (placeExists.rowCount === 0) {
      return res.status(404).json({ message: "Place not found." });
    }

    await pool.query(
      "INSERT INTO reviews(email, place_id, rating, comment) VALUES($1, $2, $3, $4)",
      [req.user.email, placeId, rating, comment],
    );

    await syncPlaceRatingInMongo(placeId);

    const updated = await pool.query(
      "SELECT place_id, name, rating FROM places WHERE place_id = $1",
      [placeId],
    );

    return res.status(201).json({
      message: "Review submitted.",
      place: updated.rows[0],
    });
  } catch (error) {
    return res.status(500).json({ message: "Failed to submit review.", error: error.message });
  }
}

module.exports = { getReviews, addReview };
