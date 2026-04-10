const PlaceGeo = require("../models/PlaceGeo");
const { pool } = require("../config/postgres");
const { rankWithML } = require("../services/mlClient");

function parseCoordinate(value, name) {
  const parsed = Number(value);
  if (!Number.isFinite(parsed)) {
    throw new Error(`${name} must be a valid number.`);
  }
  return parsed;
}

async function syncPlacesToMongo(places) {
  for (const place of places) {
    await PlaceGeo.findOneAndUpdate(
      { placeId: place.place_id },
      {
        placeId: place.place_id,
        name: place.name,
        rating: Number(place.rating || 0),
        reviewCount: Number(place.review_count || 0),
        hashtag: place.hashtag || "",
        address: place.address || "",
        wifi: !!place.wifi,
        indoor: !!place.indoor,
        outdoor: !!place.outdoor,
        location: {
          type: "Point",
          coordinates: [Number(place.longitude), Number(place.latitude)],
        },
      },
      { upsert: true, new: true, setDefaultsOnInsert: true },
    );
  }
}

function fallbackRanking(places) {
  return [...places]
    .sort((a, b) => {
      const aScore = Number(a.rating || 0) * 0.7 - Number(a.distance_m || 0) * 0.0001;
      const bScore = Number(b.rating || 0) * 0.7 - Number(b.distance_m || 0) * 0.0001;
      return bScore - aScore;
    })
    .map((place, index) => ({
      ...place,
      rank_score: Number((1 - index / Math.max(places.length, 1)).toFixed(4)),
    }));
}

async function getRecommendations(req, res) {
  let latitude;
  let longitude;

  try {
    latitude = parseCoordinate(req.query.lat, "lat");
    longitude = parseCoordinate(req.query.lng, "lng");
  } catch (error) {
    return res.status(400).json({ message: error.message });
  }

  const radius = Number(req.query.radius || 5000);

  try {
    const preferencesResult = await pool.query(
      "SELECT wifi, indoor, outdoor FROM preferences WHERE email = $1",
      [req.user.email],
    );

    const preferences =
      preferencesResult.rowCount > 0
        ? preferencesResult.rows[0]
        : { wifi: false, indoor: false, outdoor: false };

    const placesResult = await pool.query(
      `SELECT
          p.place_id,
          p.name,
          p.latitude,
          p.longitude,
          p.rating,
          p.hashtag,
          p.address,
          p.wifi,
          p.indoor,
          p.outdoor,
          COUNT(r.place_id)::int AS review_count,
          ST_Distance(
            p.geom,
            ST_SetSRID(ST_MakePoint($1, $2), 4326)::geography
          ) AS distance_m
       FROM places p
       LEFT JOIN reviews r ON r.place_id = p.place_id
       WHERE ST_DWithin(
         p.geom,
         ST_SetSRID(ST_MakePoint($1, $2), 4326)::geography,
         $3
       )
       GROUP BY p.place_id
       ORDER BY distance_m ASC`,
      [longitude, latitude, radius],
    );

    const places = placesResult.rows;

    if (places.length === 0) {
      return res.json({ places: [], source: "none" });
    }

    await syncPlacesToMongo(places);

    try {
      const mlResponse = await rankWithML({
        user_location: { lat: latitude, lng: longitude },
        preferences,
        places,
      });

      const rankedByPlaceId = new Map(
        (mlResponse.ranked_places || []).map((place) => [Number(place.place_id), place]),
      );

      const rankedPlaces = places
        .map((place) => {
          const ranked = rankedByPlaceId.get(Number(place.place_id));
          return ranked
            ? { ...place, rank_score: ranked.rank_score, distance_km: ranked.distance_km }
            : { ...place, rank_score: 0, distance_km: Number(place.distance_m) / 1000 };
        })
        .sort((a, b) => Number(b.rank_score) - Number(a.rank_score));

      return res.json({ places: rankedPlaces, source: "ml" });
    } catch (mlError) {
      return res.json({ places: fallbackRanking(places), source: "fallback", warning: mlError.message });
    }
  } catch (error) {
    return res.status(500).json({ message: "Failed to fetch recommendations.", error: error.message });
  }
}

async function getPlaceById(req, res) {
  const placeId = Number(req.params.placeId);

  if (!Number.isInteger(placeId)) {
    return res.status(400).json({ message: "Invalid place id." });
  }

  try {
    const result = await pool.query(
      "SELECT place_id, name, latitude, longitude, rating, hashtag, address, wifi, indoor, outdoor FROM places WHERE place_id = $1",
      [placeId],
    );

    if (result.rowCount === 0) {
      return res.status(404).json({ message: "Place not found." });
    }

    return res.json(result.rows[0]);
  } catch (error) {
    return res.status(500).json({ message: "Failed to fetch place.", error: error.message });
  }
}

async function getMongoNearby(req, res) {
  const latitude = Number(req.query.lat);
  const longitude = Number(req.query.lng);
  const maxDistance = Number(req.query.radius || 3000);

  if (!Number.isFinite(latitude) || !Number.isFinite(longitude)) {
    return res.status(400).json({ message: "lat and lng are required." });
  }

  try {
    const docs = await PlaceGeo.find({
      location: {
        $near: {
          $geometry: {
            type: "Point",
            coordinates: [longitude, latitude],
          },
          $maxDistance: maxDistance,
        },
      },
    })
      .limit(20)
      .lean();

    return res.json({ places: docs });
  } catch (error) {
    return res.status(500).json({ message: "Failed to query Mongo nearby.", error: error.message });
  }
}

module.exports = { getRecommendations, getPlaceById, getMongoNearby };
