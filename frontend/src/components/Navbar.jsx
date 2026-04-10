import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function Navbar() {
  const { isAuthenticated, user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <nav className="navbar">
      <div className="brand">
        <Link to="/">Study Hub</Link>
      </div>
      <div className="nav-links">
        <Link to="/">Home</Link>
        <Link to="/contact">Contact</Link>
        <Link to="/about">About</Link>
        <Link to="/map" title="Search places">
          🔍
        </Link>
        {isAuthenticated ? (
          <button className="link-like" onClick={handleLogout} type="button">
            👤 {user?.name || "Profile"} (Logout)
          </button>
        ) : (
          <Link to="/login">👤 Login</Link>
        )}
      </div>
    </nav>
  );
}

export default Navbar;
