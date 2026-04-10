import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { GoogleMap, Marker, useJsApiLoader } from "@react-google-maps/api";
import Navbar from "../components/Navbar";
import api from "../services/api";

const defaultCenter = { lat: 12.9066, lng: 77.5858 };

function MapPage() {
  const mapsApiKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY;
  const { isLoaded } = useJsApiLoader({
    id: "study-hub-map",
    googleMapsApiKey: mapsApiKey || "",
  });

  const storedCoords = useMemo(() => {
    const raw = localStorage.getItem("studyhub_coords");
    return raw ? JSON.parse(raw) : defaultCenter;
  }, []);

  const [center, setCenter] = useState(storedCoords);
  const [searchText, setSearchText] = useState("JP Nagar");
  const [places, setPlaces] = useState([]);
  const [statusText, setStatusText] = useState("Searching nearby study spots...");
  const [loading, setLoading] = useState(false);

  const fetchRecommendations = async (lat, lng) => {
    setLoading(true);
    setStatusText("Fetching ranked recommendations...");

    try {
      const response = await api.get("/places/recommendations", {
        params: { lat, lng, radius: 5000 },
      });
      setPlaces(response.data.places || []);
      const sourceLabel = response.data.source === "ml" ? "ML ranking" : "fallback ranking";
      setStatusText(`Showing ${response.data.places?.length || 0} places (${sourceLabel}).`);
    } catch (error) {
      setStatusText(error?.response?.data?.message || "Unable to fetch places.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRecommendations(center.lat, center.lng);
  }, [center.lat, center.lng]);

  const useMyLocation = () => {
    if (!navigator.geolocation) {
      setStatusText("Geolocation is not available in this browser.");
      return;
    }

    navigator.geolocation.getCurrentPosition(
      (position) => {
        const nextCenter = {
          lat: position.coords.latitude,
          lng: position.coords.longitude,
        };
        setCenter(nextCenter);
        localStorage.setItem("studyhub_coords", JSON.stringify(nextCenter));
      },
      () => setStatusText("Location permission denied. Keep using manual search."),
    );
  };

  const searchLocation = () => {
    if (!window.google || !window.google.maps || !searchText.trim()) {
      setStatusText("Google geocoder unavailable. Using current coordinates.");
      fetchRecommendations(center.lat, center.lng);
      return;
    }

    const geocoder = new window.google.maps.Geocoder();
    geocoder.geocode({ address: searchText }, (results, status) => {
      if (status === "OK" && results?.[0]?.geometry?.location) {
        const nextCenter = {
          lat: results[0].geometry.location.lat(),
          lng: results[0].geometry.location.lng(),
        };
        setCenter(nextCenter);
      } else {
        setStatusText("Unable to geocode that location. Try a nearby area.");
      }
    });
  };

  return (
    <div className="page-shell">
      <Navbar />
      <main className="map-page">
        <section className="search-panel">
          <input
            value={searchText}
            onChange={(event) => setSearchText(event.target.value)}
            placeholder="Search place (e.g. JP Nagar)"
          />
          <button type="button" className="cta-button" onClick={searchLocation}>
            Search
          </button>
          <button type="button" className="outline-button" onClick={useMyLocation}>
            Use GPS
          </button>
        </section>

        <p className="status-text">{statusText}</p>

        <section className="map-container">
          {!mapsApiKey ? (
            <div className="map-placeholder">
              Add `VITE_GOOGLE_MAPS_API_KEY` in frontend `.env` to enable map rendering.
            </div>
          ) : isLoaded ? (
            <GoogleMap mapContainerStyle={{ width: "100%", height: "100%" }} center={center} zoom={14}>
              <Marker position={center} label="You" />
              {places.map((place) => (
                <Marker
                  key={place.place_id}
                  position={{ lat: Number(place.latitude), lng: Number(place.longitude) }}
                  label={`${place.rating || 0}★`}
                />
              ))}
            </GoogleMap>
          ) : (
            <div className="map-placeholder">Loading Google Map...</div>
          )}
        </section>

        <section className="ranked-list">
          <h2>Ranked Study Spots</h2>
          {loading && <p>Loading places...</p>}
          {!loading &&
            places.map((place) => (
              <article key={place.place_id} className="place-card">
                <div>
                  <h3>
                    {place.name} {Number(place.rating || 0).toFixed(1)}★
                  </h3>
                  <p>
                    {place.hashtag || "#study"} - {place.address || "Nearby"}
                  </p>
                  <p>
                    Distance:{" "}
                    {place.distance_km
                      ? `${Number(place.distance_km).toFixed(2)} km`
                      : `${(Number(place.distance_m || 0) / 1000).toFixed(2)} km`}
                  </p>
                </div>
                <Link to={`/reviews/${place.place_id}`} className="outline-button inline-link">
                  View Reviews
                </Link>
              </article>
            ))}
          {!loading && places.length === 0 && <p>No spots found in this radius.</p>}
        </section>
      </main>
    </div>
  );
}

export default MapPage;
