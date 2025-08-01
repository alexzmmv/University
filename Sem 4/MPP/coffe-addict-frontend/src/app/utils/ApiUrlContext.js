'use client';
import { createContext, useContext } from 'react';
import getConfig from 'next/config';

// Get runtime config
const { publicRuntimeConfig } = getConfig() || {};

// Use environment variable with fallback to config or direct fallback
export const API_URL = process.env.API_BASE_URL || 
                       (publicRuntimeConfig && publicRuntimeConfig.API_BASE_URL) || 
                       "http://localhost:8000/";

// Create context
export const ApiUrlContext = createContext(API_URL);

// Hook to use the API URL
export function useApiUrl() {
  return useContext(ApiUrlContext);
}

// Custom hook for API calls with authentication
export function useApi() {
  const apiUrl = useContext(ApiUrlContext);
  
  /**
   * Make an authenticated fetch request
   * @param {string} endpoint - API endpoint
   * @param {Object} options - Fetch options
   * @param {boolean} requireAuth - Whether the endpoint requires authentication
   * @returns {Promise<any>} - API response
   */
  const fetchWithAuth = async (endpoint, options = {}, requireAuth = false) => {
    const url = `${apiUrl}${endpoint}`;
    
    // Get token if authentication is required
    let headers = { ...options.headers };
    
    if (requireAuth && typeof window !== 'undefined') {
      const token = localStorage.getItem('accessToken');
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }
    }
    
    // Make the request
    let response = await fetch(url, {
      ...options,
      headers
    });
    
    // If token expired, try to refresh it
    if (response.status === 401 && requireAuth && typeof window !== 'undefined') {
      const refreshToken = localStorage.getItem('refreshToken');
      if (refreshToken) {
        try {
          // Try to refresh the token
          const refreshResponse = await fetch(`${apiUrl}auth/refresh`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              refresh_token: refreshToken,
            }),
          });
          
          if (refreshResponse.ok) {
            const data = await refreshResponse.json();
            localStorage.setItem('accessToken', data.access_token);
            
            // Try again with new token
            headers['Authorization'] = `Bearer ${data.access_token}`;
            response = await fetch(url, {
              ...options,
              headers
            });
          }
        } catch (error) {
          console.error('Error refreshing token:', error);
        }
      }
    }
    
    return response;
  };
  
  return {
    apiUrl,
    fetchWithAuth
  };
}

// Provider component for API URL
export function ApiUrlProvider({ children }) {
  return (
    <ApiUrlContext.Provider value={API_URL}>
      {children}
    </ApiUrlContext.Provider>
  );
}