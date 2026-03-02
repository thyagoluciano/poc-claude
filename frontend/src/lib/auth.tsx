'use client';

import {createContext, useCallback, useContext, useEffect, useMemo, useState} from 'react';

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface UserData {
  username: string;
}

interface AuthState {
  user: UserData | null;
  token: string | null;
  loading: boolean;
}

interface AuthContextValue extends AuthState {
  login: (username: string, password: string) => Promise<void>;
  register: (email: string, username: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

function decodeTokenPayload(token: string): {sub?: string; exp?: number} | null {
  try {
    const parts = token.split('.');
    if (parts.length !== 3) return null;
    const payload = parts[1];
    const decoded = atob(payload.replace(/-/g, '+').replace(/_/g, '/'));
    return JSON.parse(decoded) as {sub?: string; exp?: number};
  } catch {
    return null;
  }
}

function getUserFromToken(token: string): UserData | null {
  const payload = decodeTokenPayload(token);
  if (!payload?.sub) return null;
  return {username: payload.sub};
}

function isTokenExpired(token: string): boolean {
  const payload = decodeTokenPayload(token);
  if (!payload?.exp) return true;
  return Date.now() >= payload.exp * 1000;
}

export function AuthProvider({children}: {children: React.ReactNode}) {
  const [state, setState] = useState<AuthState>({
    user: null,
    token: null,
    loading: true,
  });

  useEffect(() => {
    const storedToken = localStorage.getItem('token');
    if (!storedToken || isTokenExpired(storedToken)) {
      localStorage.removeItem('token');
      setState({user: null, token: null, loading: false});
      return;
    }

    const user = getUserFromToken(storedToken);
    if (user) {
      setState({user, token: storedToken, loading: false});
    } else {
      localStorage.removeItem('token');
      setState({user: null, token: null, loading: false});
    }
  }, []);

  const login = useCallback(async (username: string, password: string): Promise<void> => {
    const params = new URLSearchParams();
    params.append('username', username);
    params.append('password', password);

    const response = await fetch(`${BASE_URL}/auth/login`, {
      method: 'POST',
      headers: {'Content-Type': 'application/x-www-form-urlencoded'},
      body: params.toString(),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => null);
      const message =
        errorData && typeof errorData === 'object' && 'detail' in errorData
          ? String(errorData.detail)
          : 'Login failed';
      throw new Error(message);
    }

    const data = (await response.json()) as {access_token: string; token_type: string};
    const token = data.access_token;
    localStorage.setItem('token', token);

    const user = getUserFromToken(token);
    if (!user) {
      throw new Error('Invalid token received');
    }

    setState({user, token, loading: false});
  }, []);

  const register = useCallback(
    async (email: string, username: string, password: string): Promise<void> => {
      const response = await fetch(`${BASE_URL}/auth/register`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({email, username, password}),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => null);
        const message =
          errorData && typeof errorData === 'object' && 'detail' in errorData
            ? String(errorData.detail)
            : 'Registration failed';
        throw new Error(message);
      }
    },
    []
  );

  const logout = useCallback(() => {
    localStorage.removeItem('token');
    setState({user: null, token: null, loading: false});
  }, []);

  const value = useMemo<AuthContextValue>(
    () => ({
      ...state,
      login,
      register,
      logout,
      isAuthenticated: state.token !== null && state.user !== null,
    }),
    [state, login, register, logout]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
