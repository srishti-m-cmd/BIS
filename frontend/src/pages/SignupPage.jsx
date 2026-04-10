import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import { useAuth } from "../context/AuthContext";

function SignupPage() {
  const { signup } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
  });
  const [error, setError] = useState("");

  const handleChange = (event) => {
    setForm((prev) => ({ ...prev, [event.target.name]: event.target.value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");

    if (form.password !== form.confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    try {
      await signup({
        name: form.name,
        email: form.email,
        password: form.password,
      });
      navigate("/map");
    } catch (err) {
      setError(err?.response?.data?.message || "Signup failed.");
    }
  };

  return (
    <div className="page-shell">
      <Navbar />
      <main className="auth-container">
        <div className="logo-circle">Study Hub</div>
        <div className="tab-row">
          <span className="tab active">Signup</span>
          <Link className="tab inactive" to="/login">
            Login
          </Link>
        </div>
        <form onSubmit={handleSubmit} className="auth-form">
          <label>
            Name
            <input type="text" name="name" value={form.name} onChange={handleChange} required />
          </label>
          <label>
            Email
            <input type="email" name="email" value={form.email} onChange={handleChange} required />
          </label>
          <label>
            Password
            <input type="password" name="password" value={form.password} onChange={handleChange} required />
          </label>
          <label>
            Confirm Password
            <input
              type="password"
              name="confirmPassword"
              value={form.confirmPassword}
              onChange={handleChange}
              required
            />
          </label>
          {error && <p className="error-text">{error}</p>}
          <button type="submit" className="cta-button">
            Sign Up
          </button>
          <button type="button" className="outline-button">
            Continue with Google
          </button>
        </form>
      </main>
    </div>
  );
}

export default SignupPage;
