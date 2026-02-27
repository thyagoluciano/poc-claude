"use client";

import {
  createContext,
  useContext,
  useState,
  useEffect,
  useCallback,
  type ReactNode,
} from "react";
import { apiPost } from "./api";

interface User {
  id: number;
  username: string;
  email: string;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

interface AuthContextValue extends AuthState {
  login: (username: string, password: string) => Promise<void>;
  register: (
    username: string,
    email: string,
    password: string
  ) => Promise<void>;
  logout: () => void;
}

interface LoginResponse {
  access_token: string;
  token_type: string;
}

interface RegisterResponse {
  id: number;
  username: string;
  email: string;
}

interface TokenPayload {
  sub: string;
  exp: number;
}

const AuthContext = createContext<AuthContextValue | null>(null);

function parseToken(token: string): TokenPayload | null {
  try {
    const payload = token.split(".")[1];
    const decoded = atob(payload);
    return JSON.parse(decoded) as TokenPayload;
  } catch {
    return null;
  }
}

function isTokenExpired(token: string): boolean {
  const payload = parseToken(token);
  if (!payload) return true;
  return Date.now() >= payload.exp * 1000;
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<AuthState>({
    user: null,
    token: null,
    isAuthenticated: false,
    isLoading: true,
  });

  useEffect(() => {
    const token = localStorage.getItem("token");
    const storedUser = localStorage.getItem("user");

    if (token && !isTokenExpired(token) && storedUser) {
      try {
        const user = JSON.parse(storedUser) as User;
        setState({
          user,
          token,
          isAuthenticated: true,
          isLoading: false,
        });
      } catch {
        localStorage.removeItem("token");
        localStorage.removeItem("user");
        setState((prev) => ({ ...prev, isLoading: false }));
      }
    } else {
      if (token) {
        localStorage.removeItem("token");
        localStorage.removeItem("user");
      }
      setState((prev) => ({ ...prev, isLoading: false }));
    }
  }, []);

  const login = useCallback(async (username: string, password: string) => {
    const formBody = new URLSearchParams();
    formBody.append("username", username);
    formBody.append("password", password);

    const API_BASE_URL =
      process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: formBody.toString(),
    });

    if (!response.ok) {
      const errorBody = await response.json().catch(() => null);
      const message =
        (errorBody as { detail?: string } | null)?.detail ??
        "Invalid credentials";
      throw new Error(message);
    }

    const data = (await response.json()) as LoginResponse;
    const token = data.access_token;

    const payload = parseToken(token);
    const user: User = {
      id: 0,
      username: payload?.sub ?? username,
      email: "",
    };

    localStorage.setItem("token", token);
    localStorage.setItem("user", JSON.stringify(user));

    setState({
      user,
      token,
      isAuthenticated: true,
      isLoading: false,
    });
  }, []);

  const register = useCallback(
    async (username: string, email: string, password: string) => {
      await apiPost<RegisterResponse>("/auth/register", {
        username,
        email,
        password,
      });
    },
    []
  );

  const logout = useCallback(() => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    setState({
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,
    });
    window.location.href = "/login";
  }, []);

  return (
    <AuthContext.Provider
      value={{
        ...state,
        login,
        register,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
