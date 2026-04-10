CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE IF NOT EXISTS users (
  email VARCHAR(255) PRIMARY KEY,
  name VARCHAR(150) NOT NULL,
  password VARCHAR(255) NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS places (
  place_id SERIAL PRIMARY KEY,
  created_by_email VARCHAR(255) REFERENCES users(email) ON DELETE SET NULL,
  name VARCHAR(255) NOT NULL UNIQUE,
  latitude DOUBLE PRECISION NOT NULL,
  longitude DOUBLE PRECISION NOT NULL,
  geom GEOGRAPHY(POINT, 4326)
    GENERATED ALWAYS AS (
      ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)::geography
    ) STORED,
  address VARCHAR(255) DEFAULT '',
  hashtag VARCHAR(120) DEFAULT '',
  wifi BOOLEAN DEFAULT FALSE,
  indoor BOOLEAN DEFAULT FALSE,
  outdoor BOOLEAN DEFAULT FALSE,
  rating NUMERIC(3, 2) DEFAULT 0 CHECK (rating >= 0 AND rating <= 5),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS preferences (
  email VARCHAR(255) PRIMARY KEY REFERENCES users(email) ON DELETE CASCADE,
  wifi BOOLEAN DEFAULT FALSE,
  indoor BOOLEAN DEFAULT FALSE,
  outdoor BOOLEAN DEFAULT FALSE,
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS reviews (
  review_id SERIAL PRIMARY KEY,
  email VARCHAR(255) REFERENCES users(email) ON DELETE CASCADE,
  place_id INT REFERENCES places(place_id) ON DELETE CASCADE,
  rating NUMERIC(2, 1) NOT NULL CHECK (rating >= 0 AND rating <= 5),
  comment TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_places_geom ON places USING GIST (geom);
CREATE INDEX IF NOT EXISTS idx_reviews_place_id ON reviews(place_id);

CREATE OR REPLACE FUNCTION update_place_average_rating()
RETURNS TRIGGER AS $$
DECLARE
  affected_place_id INT;
BEGIN
  affected_place_id := COALESCE(NEW.place_id, OLD.place_id);

  UPDATE places
  SET rating = COALESCE(
    (SELECT ROUND(AVG(rating)::numeric, 2) FROM reviews WHERE place_id = affected_place_id),
    0
  )
  WHERE place_id = affected_place_id;

  RETURN NULL;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_update_place_average_rating ON reviews;
CREATE TRIGGER trg_update_place_average_rating
AFTER INSERT OR UPDATE OR DELETE ON reviews
FOR EACH ROW
EXECUTE FUNCTION update_place_average_rating();
