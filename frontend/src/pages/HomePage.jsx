import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import { useAuth } from "../context/AuthContext";

function HomePage() {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();
  const [showPermissionPopup, setShowPermissionPopup] = useState(false);
  const [locationText, setLocationText] = useState("Location not selected");

  const handleFind = () => {
    if (isAuthenticated) {
      navigate("/map");
      return;
    }

    navigate("/login");
  };

  const requestLocation = () => {
    setShowPermissionPopup(true);
  };

  const allowLocation = () => {
    if (!navigator.geolocation) {
      setLocationText("Geolocation is not supported in this browser.");
      setShowPermissionPopup(false);
      return;
    }

    navigator.geolocation.getCurrentPosition(
      (position) => {
        const { latitude, longitude } = position.coords;
        localStorage.setItem("studyhub_coords", JSON.stringify({ lat: latitude, lng: longitude }));
        setLocationText(`Selected: ${latitude.toFixed(4)}, ${longitude.toFixed(4)}`);
        setShowPermissionPopup(false);
      },
      () => {
        setLocationText("Permission denied. Enter location manually on map page.");
        setShowPermissionPopup(false);
      },
    );
  };

  return (
    <div className="page-shell">
      <Navbar />

      <main className="hero">
        <h1>Welcome to StudyHub.com</h1>
        <p>Discover calm cafes, libraries, and study corners around you.</p>
        <button type="button" className="cta-button" onClick={handleFind}>
          Find!
        </button>

        <section className="location-box">
          <h2>Nearby Location</h2>
          <p className="icon-line">
            📍 GPS enabled search
          </p>
          <p className="icon-line">🗺️ Map-based recommendations</p>
          <p>{locationText}</p>
          <button type="button" className="outline-button" onClick={requestLocation}>
            Enable Location Permission
          </button>
        </section>
      </main>

      {showPermissionPopup && (
        <div className="popup-backdrop">
          <div className="popup">
            <h3>Allow location access?</h3>
            <p>Study Hub uses your GPS to suggest nearby study spots.</p>
            <button type="button" className="cta-button" onClick={allowLocation}>
              Allow
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default HomePage;
