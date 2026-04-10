# Study Hub

Study Hub is a full-stack local search and recommendation web app that helps students discover nearby study spots.  
It uses geospatial filtering (`PostGIS ST_DWithin`) and an ML ranking service (Flask + KNN + Haversine).

## Tech Stack

- Frontend: React.js (Vite), Google Maps API, HTML/CSS/JS
- Backend: Node.js + Express
- ML Microservice: Python Flask, NumPy, Pandas, Scikit-learn
- Databases:
  - PostgreSQL + PostGIS (core transactional data)
  - MongoDB + GeoJSON (document/geo mirror)

## Folder Structure

```text
.
├── backend
│   ├── scripts
│   ├── sql
│   └── src
├── frontend
│   └── src
├── infra
│   └── docker-compose.yml
└── ml-service
```

## PostgreSQL Schema

- `users` (`email` PK, `name`, `password`)
- `places` (`place_id` PK, `name`, `latitude`, `longitude`, `rating`, plus geo/metadata)
- `reviews` (`email` FK -> users, `place_id` FK -> places, `rating`, `comment`)
- `preferences` (`email` FK -> users, `wifi`, `indoor`, `outdoor`)

Includes trigger-based auto-update for average `places.rating` when reviews are inserted/updated/deleted.

## Setup

1. Copy environment files.

```bash
cp .env.example .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

2. Start PostgreSQL (PostGIS) and MongoDB.

```bash
docker compose -f infra/docker-compose.yml up -d
```

3. Install Node dependencies.

```bash
npm install
```

4. Initialize and seed PostgreSQL.

```bash
npm run db:init
npm run db:seed
```

5. Install Python dependencies.

```bash
cd ml-service
pip install -r requirements.txt
cd ..
```

6. Start services in separate terminals.

```bash
npm run dev:backend
npm run dev:frontend
```

```bash
cd ml-service
python app.py
```

## Default Ports

- Frontend: `http://localhost:5173`
- Backend: `http://localhost:4000`
- ML service: `http://localhost:5001`

## Core API Endpoints

- `POST /api/auth/signup`
- `POST /api/auth/login`
- `GET /api/preferences` (protected)
- `PUT /api/preferences` (protected)
- `GET /api/places/recommendations?lat=..&lng=..&radius=..` (protected)
- `GET /api/places/:placeId/reviews` (protected)
- `POST /api/places/:placeId/reviews` (protected)

## Notes

- Google Maps requires a valid API key in `frontend/.env` (`VITE_GOOGLE_MAPS_API_KEY`).
- Mock geodata is seeded from `backend/sql/seed.sql`.
