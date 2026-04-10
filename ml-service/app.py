from flask import Flask, jsonify, request
from sklearn.neighbors import NearestNeighbors
import numpy as np
import pandas as pd

app = Flask(__name__)


def haversine_distance_km(lat1, lng1, lat2, lng2):
    radius_km = 6371.0
    lat1_rad, lng1_rad = np.radians(lat1), np.radians(lng1)
    lat2_rad, lng2_rad = np.radians(lat2), np.radians(lng2)
    dlat = lat2_rad - lat1_rad
    dlng = lng2_rad - lng1_rad
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlng / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return radius_km * c


@app.get("/health")
def health():
    return jsonify({"status": "ok", "service": "study-hub-ml"})


@app.post("/rank")
def rank_places():
    body = request.get_json(silent=True) or {}
    user_location = body.get("user_location", {})
    user_lat = float(user_location.get("lat", 0))
    user_lng = float(user_location.get("lng", 0))
    preferences = body.get("preferences", {})
    places = body.get("places", [])

    if not places:
        return jsonify({"ranked_places": []})

    dataframe = pd.DataFrame(places)
    if dataframe.empty:
        return jsonify({"ranked_places": []})

    dataframe["latitude"] = dataframe["latitude"].astype(float)
    dataframe["longitude"] = dataframe["longitude"].astype(float)
    dataframe["rating"] = dataframe.get("rating", 0).astype(float).fillna(0)
    dataframe["review_count"] = dataframe.get("review_count", 0).astype(float).fillna(0)
    dataframe["distance_km"] = dataframe.apply(
        lambda row: haversine_distance_km(user_lat, user_lng, row["latitude"], row["longitude"]),
        axis=1,
    )

    coordinate_matrix = dataframe[["latitude", "longitude"]].to_numpy()
    neighbors = min(len(dataframe), 10)
    knn = NearestNeighbors(n_neighbors=neighbors)
    knn.fit(coordinate_matrix)
    _, neighbor_indices = knn.kneighbors(np.array([[user_lat, user_lng]]))
    ranked = dataframe.iloc[neighbor_indices[0]].copy()

    max_distance = max(ranked["distance_km"].max(), 1)
    ranked["distance_score"] = 1 - (ranked["distance_km"] / max_distance)
    ranked["rating_score"] = ranked["rating"] / 5
    ranked["review_score"] = np.clip(ranked["review_count"] / 20, 0, 1)

    pref_bonus = np.zeros(len(ranked))
    if preferences.get("wifi", False):
        pref_bonus += ranked.get("wifi", False).astype(int) * 0.08
    if preferences.get("indoor", False):
        pref_bonus += ranked.get("indoor", False).astype(int) * 0.08
    if preferences.get("outdoor", False):
        pref_bonus += ranked.get("outdoor", False).astype(int) * 0.08

    ranked["rank_score"] = (
        ranked["distance_score"] * 0.45
        + ranked["rating_score"] * 0.35
        + ranked["review_score"] * 0.15
        + pref_bonus * 0.05
    )

    ranked = ranked.sort_values("rank_score", ascending=False)
    columns = [
        "place_id",
        "name",
        "latitude",
        "longitude",
        "rating",
        "review_count",
        "distance_km",
        "rank_score",
    ]
    ranked["distance_km"] = ranked["distance_km"].round(3)
    ranked["rank_score"] = ranked["rank_score"].round(4)
    return jsonify({"ranked_places": ranked[columns].to_dict(orient="records")})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
