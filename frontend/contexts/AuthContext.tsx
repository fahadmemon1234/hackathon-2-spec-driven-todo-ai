'use client';

import React, {
  createContext,
  useContext,
  useEffect,
  useState,
  ReactNode,
} from 'react';

interface AuthContextType {
  user: any | null;
  loading: boolean;
  signIn: (email: string, password: string) => Promise<void>;
  signOut: () => Promise<void>;
  signUp: (email: string, password: string) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider = ({ children }: AuthProviderProps) => {
  const [user, setUser] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);

  // Load session on app start
  useEffect(() => {
    const loadSession = async () => {
      try {
        // First check if we have a token in localStorage
        const token = localStorage.getItem('auth-token');
        if (token) {
          // Use the stored user data if available
          const userData = localStorage.getItem('user-data');
          if (userData) {
            setUser(JSON.parse(userData));
          }
        } else {
          // If no token in localStorage, try to get session from API
          const res = await fetch('/api/auth/session');
          if (res.ok) {
            const data = await res.json();
            if (data?.user) {
              setUser(data.user);
              // Store in localStorage for API client access
              // Note: We can't get the token from the session endpoint, so we assume it exists
              // In a real implementation, the session endpoint would return the token as well
              localStorage.setItem('user-data', JSON.stringify(data.user));
            }
          }
        }
      } catch (err) {
        console.error('Failed to load session', err);
      } finally {
        setLoading(false);
      }
    };

    loadSession();
  }, []);

  const signIn = async (email: string, password: string) => {
    const res = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });

    const result = await res.json();

    if (!res.ok) {
      throw new Error(result.error?.message || 'Login failed');
    }

    // Store token in localStorage for API client access
    localStorage.setItem('auth-token', result.token);
    localStorage.setItem('user-data', JSON.stringify(result.user));

    // Update user state
    setUser(result.user);
  };

  const signOut = async () => {
    await fetch('/api/auth/logout', { method: 'POST' });
    // Clear local storage as well
    localStorage.removeItem('auth-token');
    localStorage.removeItem('user-data');
    setUser(null);
  };

  const signUp = async (email: string, password: string) => {
    const res = await fetch('/api/auth/signup', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });

    const result = await res.json();

    if (!res.ok) {
      throw new Error(result.error?.message || 'Signup failed');
    }

    // Store token in localStorage for API client access
    localStorage.setItem('auth-token', result.token);
    localStorage.setItem('user-data', JSON.stringify(result.user));

    // Update user state
    setUser(result.user);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        signIn,
        signOut,
        signUp,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
