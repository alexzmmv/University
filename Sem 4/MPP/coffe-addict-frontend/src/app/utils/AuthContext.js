import { createContext, useContext, useState, useEffect } from 'react';
import getConfig from 'next/config';
import { API_URL } from './ApiUrlContext'; // Use the same API_URL defined in ApiUrlContext

const AuthContext = createContext(null);

// Helper function to set cookies
const setCookie = (name, value, days = 7) => {
  if (typeof window === 'undefined') return;
  
  const expires = new Date();
  expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
  document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/;SameSite=Strict`;
};

// Helper function to remove a cookie
const removeCookie = (name) => {
  if (typeof window === 'undefined') return;
  document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/`;
};

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Check if user is logged in on page load
    const loadUser = async () => {
      try {
        const token = localStorage.getItem('accessToken');
        if (!token) {
          setLoading(false);
          return;
        }

        // Fetch user profile
        const response = await fetch(`${API_URL}auth/users/me`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (response.ok) {
          const userData = await response.json();
          setUser(userData);
        } else {
          // Token might be expired - try to refresh
          const refreshed = await refreshToken();
          if (!refreshed) {
            // If refresh failed, clear tokens
            logout();
          }
        }
      } catch (err) {
        console.error('Error loading user:', err);
        setError('Failed to load user profile');
      } finally {
        setLoading(false);
      }
    };

    loadUser();
  }, []);

  const login = async (username, password) => {
    try {
      setError(null);
      const response = await fetch(`${API_URL}auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username,
          password,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Login failed');
      }

      const data = await response.json();
      
      // Debug: Log the response data
      console.log('Login API response:', data);
      
      // Check if 2FA is required
      if (data.requires_2fa) {
        console.log('2FA required - returning 2FA data');
        return {
          requires2FA: true,
          jobId: data.job_id,
          message: data.message,
          phoneHint: data.phone_number_hint
        };
      }
      
      // Regular login - store tokens and fetch user profile
      localStorage.setItem('accessToken', data.access_token);
      localStorage.setItem('refreshToken', data.refresh_token);
      setCookie('accessToken', data.access_token);
      setCookie('refreshToken', data.refresh_token);
      
      // Fetch user profile
      const userResponse = await fetch(`${API_URL}auth/users/me`, {
        headers: {
          'Authorization': `Bearer ${data.access_token}`
        }
      });
      
      if (userResponse.ok) {
        const userData = await userResponse.json();
        setUser(userData);
        return { success: true };
      } else {
        throw new Error('Failed to fetch user profile');
      }
    } catch (err) {
      console.error('Login error:', err);
      setError(err.message || 'Login failed. Please try again.');
      return { success: false, error: err.message };
    }
  };

  const register = async (username, email, password, phone_number, enable_2fa = false) => {
    try {
      setError(null);
      const response = await fetch(`${API_URL}auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username,
          email,
          password,
          phone_number,
          enable_2fa,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Registration failed');
      }

      // Registration successful, now login
      return await login(username, password);
    } catch (err) {
      console.error('Registration error:', err);
      setError(err.message || 'Registration failed. Please try again.');
      return false;
    }
  };

  const refreshToken = async () => {
    try {
      const refreshToken = localStorage.getItem('refreshToken');
      if (!refreshToken) return false;

      const response = await fetch(`${API_URL}auth/refresh`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          refresh_token: refreshToken,
        }),
      });

      if (!response.ok) {
        return false;
      }

      const data = await response.json();
      localStorage.setItem('accessToken', data.access_token);
      localStorage.setItem('refreshToken', data.refresh_token);
      setCookie('accessToken', data.access_token);
      setCookie('refreshToken', data.refresh_token);
      return true;
    } catch (err) {
      console.error('Error refreshing token:', err);
      return false;
    }
  };

  const logout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    removeCookie('accessToken');
    removeCookie('refreshToken');
    setUser(null);
  };

  const verify2FA = async (jobId, code) => {
    try {
      setError(null);
      const response = await fetch(`${API_URL}auth/verify-2fa`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          job_id: jobId,
          code: code,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || '2FA verification failed');
      }

      const data = await response.json();
      
      // Store tokens and fetch user profile
      localStorage.setItem('accessToken', data.access_token);
      localStorage.setItem('refreshToken', data.refresh_token);
      setCookie('accessToken', data.access_token);
      setCookie('refreshToken', data.refresh_token);
      
      // Fetch user profile
      const userResponse = await fetch(`${API_URL}auth/users/me`, {
        headers: {
          'Authorization': `Bearer ${data.access_token}`
        }
      });
      
      if (userResponse.ok) {
        const userData = await userResponse.json();
        setUser(userData);
        return { success: true };
      } else {
        throw new Error('Failed to fetch user profile');
      }
    } catch (err) {
      console.error('2FA verification error:', err);
      setError(err.message || '2FA verification failed. Please try again.');
      return { success: false, error: err.message };
    }
  };

  const value = {
    user,
    loading,
    error,
    login,
    register,
    logout,
    refreshToken,
    verify2FA,
    isAuthenticated: !!user,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === null) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
