import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';

interface AuthContextType {
  user: any;
  token: string | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  authenticatedFetch: (url: string, options?: RequestInit) => Promise<Response>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<any>(null);
  const [token, setToken] = useState<string | null>(localStorage.getItem('nexus_jwt_token'));
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const savedUser = localStorage.getItem('nexus_user');
    if (savedUser && token) {
      try {
        setUser(JSON.parse(savedUser));
      } catch (e) {
        localStorage.removeItem('nexus_user');
      }
    }
    setLoading(false);
  }, [token]);

  const login = async (email: string, password: string) => {
    const res = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });

    const data = await res.json();
    if (data.success) {
      setToken(data.token);
      setUser(data.user);
      localStorage.setItem('nexus_jwt_token', data.token);
      localStorage.setItem('nexus_user', JSON.stringify(data.user));
    } else {
      throw new Error(data.error || 'Authentication failed');
    }
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem('nexus_jwt_token');
    localStorage.removeItem('nexus_user');
  };

  const authenticatedFetch = useCallback(async (url: string, options: RequestInit = {}) => {
    const headers = {
      ...(options.headers || {}),
      'Authorization': `Bearer ${token}`
    } as Record<string, string>;

    try {
      const res = await fetch(url, { ...options, headers });
      if (res.status === 401 || res.status === 403) {
        logout();
      }
      return res;
    } catch (err) {
      console.error("Network fetch failed:", err);
      // Return a simulated offline/error response to prevent unhandled promise rejections
      return new Response(JSON.stringify({ 
        success: false, 
        error: "OFFLINE", 
        message: "Failed to communicate with host server." 
      }), {
        status: 503,
        headers: { 'Content-Type': 'application/json' }
      });
    }
  }, [token]);

  return (
    <AuthContext.Provider value={{ user, token, loading, login, logout, authenticatedFetch }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};