import { createContext, useContext, useMemo, useState } from "react";
import api from "../services/api";

const AuthContext = createContext(null);

function readStoredUser() {
  const raw = localStorage.getItem("studyhub_user");
  return raw ? JSON.parse(raw) : null;
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(readStoredUser);
  const [token, setToken] = useState(localStorage.getItem("studyhub_token"));

  const persistAuth = (authToken, authUser) => {
    localStorage.setItem("studyhub_token", authToken);
    localStorage.setItem("studyhub_user", JSON.stringify(authUser));
    setToken(authToken);
    setUser(authUser);
  };

  const clearAuth = () => {
    localStorage.removeItem("studyhub_token");
    localStorage.removeItem("studyhub_user");
    setToken(null);
    setUser(null);
  };

  const login = async (payload) => {
    const response = await api.post("/auth/login", payload);
    persistAuth(response.data.token, response.data.user);
    return response.data;
  };

  const signup = async (payload) => {
    const response = await api.post("/auth/signup", payload);
    persistAuth(response.data.token, response.data.user);
    return response.data;
  };

  const value = useMemo(
    () => ({
      user,
      token,
      isAuthenticated: Boolean(token),
      login,
      signup,
      logout: clearAuth,
    }),
    [token, user],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used inside AuthProvider");
  }
  return context;
}
