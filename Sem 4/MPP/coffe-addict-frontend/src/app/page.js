"use client"
import { useState, useEffect, useRef, useCallback } from "react";
import { Header } from "./components/homeWindow/Header";
import { Footer } from "./components/Footer";
import { CoffeeShopList } from "./components/homeWindow/CoffeShopList";
import { SearchFilterSortSection } from "./components/homeWindow/SearchFilterSortSection";
import { ConnectionStatus } from "./components/ConnectionStatus";
import getConfig from 'next/config';
import axios from "axios";

// Get runtime config
const { publicRuntimeConfig } = getConfig() || {};

// Use environment variable with fallback to config or direct fallback
const API_URL = process.env.API_BASE_URL || (publicRuntimeConfig && publicRuntimeConfig.API_BASE_URL) || "http://localhost:8000/";
const CHECKTIME = 30000; 
const PAGE_SIZE = 10; 

// Create a custom Axios instance with improved error handling
const axiosInstance = axios.create({
  timeout: 15000, // Set a reasonable timeout
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
});

// Track last request times to prevent duplicates
let lastRequestTime = {};

// Configure request interceptor with proper error handling
axiosInstance.interceptors.request.use(
  (config) => {
    // Create a unique key for this request
    const requestKey = `${config.url}?${new URLSearchParams(config.params || {}).toString()}`;
    const now = Date.now();
    
    // Prevent duplicate requests within 2 seconds
    if (lastRequestTime[requestKey] && now - lastRequestTime[requestKey] < 2000) {
      const cancelError = new axios.Cancel('Duplicate request prevented');
      cancelError.canceled = true;
      return Promise.reject(cancelError);
    }
    
    // Track this request time
    lastRequestTime[requestKey] = now;
    return config;
  },
  (error) => {
    // Properly format the rejection for the interceptor
    return Promise.reject(error);
  }
);

// Add a response interceptor for better error handling
axiosInstance.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Handle request cancellation gracefully
    if (axios.isCancel(error) || error.canceled) {
      const cancelError = new Error('Request was cancelled');
      cancelError.canceled = true;
      return Promise.reject(cancelError);
    }
    
    // Handle network errors
    if (error.message === 'Network Error') {
      console.warn('Network error detected');
      const networkError = new Error('Network Error');
      networkError.isNetworkError = true;
      return Promise.reject(networkError);
    }
    
    // Handle timeout errors
    if (error.code === 'ECONNABORTED') {
      console.warn('Request timeout');
      const timeoutError = new Error('Request timeout');
      timeoutError.isTimeout = true;
      return Promise.reject(timeoutError);
    }
    
    // Return other errors normally
    return Promise.reject(error);
  }
);

export default function Page() {
  const [coffeeShops, setCoffeeShops] = useState([]);
  const [filteredShops, setFilteredShops] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [userLocation, setUserLocation] = useState({latitude: 0, longitude: 0});
  //server status
  const [isServerReachable, setIsServerReachable] = useState(true);
  const [isOnline, setIsOnline] = useState(true);
  
  // Pagination states
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);
  
  // Refs for observer and request tracking
  const observer = useRef();
  const checkServerTimeoutRef = useRef(null);
  const loadMoreTimeoutRef = useRef(null);

  const isMountedRef = useRef(true);

  const checkServerStatus = useCallback(async () => {
    if (!isMountedRef.current) return false;
    
    try {
      await axiosInstance.get(`${API_URL}health`, { timeout: 5000 });
      if (isMountedRef.current) {
        setIsServerReachable(true);
      }
      return true;
    } catch (error) {
      if (error.canceled) {
        return isServerReachable;
      }
      
      if (isMountedRef.current) {
        setIsServerReachable(false);
      }
      return false;
    }
  }, [isServerReachable]);

  const loadMoreCoffeeShops = useCallback(async () => {
    if (!navigator.onLine || !isServerReachable || !hasMore || loadingMore) return;
    
    if (loadMoreTimeoutRef.current) {
      clearTimeout(loadMoreTimeoutRef.current);
      loadMoreTimeoutRef.current = null;
    }
    
    setLoadingMore(true);
    
    try {
      const nextPage = page + 1;
      
      const response = await axiosInstance.get(API_URL+'coffee-shops', {
        params: {
          latitude: userLocation.latitude, 
          longitude: userLocation.longitude,
          page: nextPage,
          page_size: PAGE_SIZE
        }
      });
      
      if (!isMountedRef.current) return;
      
      if (response.data && response.data.coffee_shops) {
        const newShops = response.data.coffee_shops.map(shop => ({
          id: shop.public_id,
          name: shop.name,
          rating: shop.rating.toString(),
          distance: `${shop.distance.toFixed(1)} km`,
          status: shop.status,
          image: shop.image
        }));
        
        // If no shops returned, we've reached the end
        if (newShops.length === 0) {
          setHasMore(false);
          return;
        }
        
        // Check for duplicate shops by creating a set of existing IDs
        const existingShopIdsSet = new Set(coffeeShops.map(shop => shop.id));
        
        // Filter out any shops that are already in our list
        const uniqueNewShops = newShops.filter(shop => !existingShopIdsSet.has(shop.id));
        
        // If all returned shops were duplicates
        if (uniqueNewShops.length === 0) {
          // If we got a full page of results, try the next page
          if (newShops.length >= PAGE_SIZE) {
            setPage(nextPage);
            loadMoreTimeoutRef.current = setTimeout(loadMoreCoffeeShops, 1000);
            return;
          } else {
            // Otherwise we've reached the end
            setHasMore(false);
            return;
          }
        }
        
        // Add new shops to our list and update localStorage
        setCoffeeShops(prevShops => {
          const updatedShops = [...prevShops, ...uniqueNewShops];
          localStorage.setItem('coffeeShops', JSON.stringify(updatedShops));
          return updatedShops;
        });
        
        // Update the filtered list with the new shops
        setFilteredShops(prevFilteredShops => [...prevFilteredShops, ...uniqueNewShops]);
        
        // Update page number
        setPage(nextPage);
        
        // Check if there are more pages based on pagination info
        setHasMore(response.data.pagination?.has_next || false);
      } else {
        setHasMore(false);
      }
    } catch (error) {
      if (error.canceled) {
        return;
      }
      
      console.error('Error loading more coffee shops:', error);
      setHasMore(false);
    } finally {
      if (isMountedRef.current) {
        setLoadingMore(false);
      }
    }
  }, [page, userLocation.latitude, userLocation.longitude, isServerReachable, hasMore, loadingMore, coffeeShops, API_URL]);

  const lastShopElementRef = useCallback(node => {
    if (loadingMore || !node) return;
    
    if (observer.current) observer.current.disconnect();
    
    let observerTriggered = false;
    
    observer.current = new IntersectionObserver(entries => {
      if (entries[0].isIntersecting && hasMore && !loadingMore && !observerTriggered) {
        observerTriggered = true;
        setTimeout(() => {
          if (isMountedRef.current) {
            loadMoreCoffeeShops();
            observerTriggered = false;
          }
        }, 300);
      }
    }, { threshold: 0.5 });
    
    observer.current.observe(node);
  }, [hasMore, loadingMore, loadMoreCoffeeShops]);

  useEffect(() => {
    const getLocation = () => {
      if (navigator.geolocation) {
        const geoOptions = {
          enableHighAccuracy: true,
          timeout: 5000,
          maximumAge: 60000
        };
        
        navigator.geolocation.getCurrentPosition(
          (position) => {
            if (!isMountedRef.current) return;
            
            const userLatitude = position.coords.latitude;
            const userLongitude = position.coords.longitude;
            
            setUserLocation({
              latitude: userLatitude,
              longitude: userLongitude
            });
            
            fetchCoffeeShops(userLatitude, userLongitude);
          },
          (error) => {
            console.error('Error getting location:', error);
            if (!isMountedRef.current) return;
            
            setUserLocation({
              latitude: 46.770439, // Default location (Cluj-Napoca)
              longitude: 23.591423
            });
            fetchCoffeeShops(46.770439, 23.591423);
          },
          geoOptions
        );
      } else {
        console.error('Geolocation is not supported by this browser.');
        if (!isMountedRef.current) return;
        
        setUserLocation({
          latitude: 46.770439, // Default location (Cluj-Napoca)
          longitude: 23.591423
        });
        fetchCoffeeShops(46.770439, 23.591423);
      }
    };

    const fetchCoffeeShops = async (latitude, longitude) => {
      const serverStatus = await checkServerStatus();
      
      if (!isMountedRef.current) return;
            
      if (!navigator.onLine || !serverStatus) {
        loadFromLocalStorage();
        return;
      }
      
      setIsLoading(true);
      
      try {
        const response = await axiosInstance.get(API_URL+'coffee-shops', {
          params: {
            latitude, 
            longitude,
            page: 1,
            page_size: PAGE_SIZE
          }
        });
        
        if (!isMountedRef.current) return;
        
        if (response.status !== 200) {
          setCoffeeShops([]);
          setFilteredShops([]);
          setHasMore(false);
          return;
        }
          
        if (response.data && response.data.coffee_shops) {
          const shops = response.data.coffee_shops.map(shop => ({
            id: shop.public_id,
            name: shop.name,
            rating: shop.rating.toString(),
            distance: `${shop.distance.toFixed(1)} km`,
            status: shop.status,
            image: shop.image
          }));
          
          const uniqueShops = Array.from(
            new Map(shops.map(shop => [shop.id, shop])).values()
          );
          
          // Check if there are more pages based on pagination info
          setHasMore(response.data.pagination?.has_next || false);
          
          localStorage.setItem('coffeeShops', JSON.stringify(uniqueShops));
          
          setCoffeeShops(uniqueShops);
          setFilteredShops(uniqueShops);
          setPage(1);
        } else {
          setHasMore(false);
        }
      } catch (error) {
        if (error.canceled) {
          return;
        }
        
        console.error('Error fetching coffee shops:', error);
        setIsServerReachable(false);
        loadFromLocalStorage();
      } finally {
        if (isMountedRef.current) {
          setIsLoading(false);
        }
      }
    };
    
    const loadFromLocalStorage = () => {
      try {
        const storedShops = localStorage.getItem('coffeeShops');
        if (storedShops) {
          const parsedShops = JSON.parse(storedShops);
          const uniqueShops = Array.from(
            new Map(parsedShops.map(shop => [shop.id, shop])).values()
          );
          setCoffeeShops(uniqueShops);
          setFilteredShops(uniqueShops);
        } else {
          console.error('No coffee shops found in local storage.');
        }
      } catch (error) {
        console.error('Error loading coffee shops from local storage:', error);
        setFilteredShops([]);
      } finally {
        if (isMountedRef.current) {
          setIsLoading(false);
        }
      }
    };
    
    const startServerChecks = () => {
      checkServerStatus();  
      checkServerTimeoutRef.current = setInterval(checkServerStatus, CHECKTIME);
    };

    isMountedRef.current = true;
    
    getLocation();
    startServerChecks();
    
    const handleOnlineStatus = () => {
      if (isMountedRef.current) {
        setIsOnline(navigator.onLine);
      }
    };
    
    window.addEventListener('online', handleOnlineStatus);
    window.addEventListener('offline', handleOnlineStatus);
    
    return () => {
      isMountedRef.current = false;
      
      if (checkServerTimeoutRef.current) {
        clearInterval(checkServerTimeoutRef.current);
      }
      
      if (loadMoreTimeoutRef.current) {
        clearTimeout(loadMoreTimeoutRef.current);
      }
      
      if (observer.current) {
        observer.current.disconnect();
      }
      
      window.removeEventListener('online', handleOnlineStatus);
      window.removeEventListener('offline', handleOnlineStatus);
    };
  }, [checkServerStatus]);

  const handleFilteredResultsChange = useCallback((filteredResults) => {
    const uniqueFilteredResults = Array.from(
      new Map(filteredResults.map(shop => [shop.id, shop])).values()
    );
    
    setFilteredShops(uniqueFilteredResults);
    setPage(1);
    setHasMore(true);
  }, []);

  return (
    <div className="flex flex-col min-h-screen bg-[#fdf8f5]">
      <ConnectionStatus isServerReachable={isServerReachable} />
      <Header />
      <main className="flex-1 p-4 pb-20">
        <SearchFilterSortSection 
          onlineFiltering={isOnline && isServerReachable}
          allShops={coffeeShops} 
          onFilteredResultsChange={handleFilteredResultsChange}
          userLocation={userLocation}
          API_URL={API_URL}
        />
        
        {process.env.NODE_ENV === 'development' && (
          <div className="text-xs text-gray-400 mb-2">
            Loaded shops: {filteredShops.length} | Page: {page} | Has more: {hasMore ? 'Yes' : 'No'}
          </div>
        )}
        
        <CoffeeShopList 
          shops={filteredShops} 
          isLoading={isLoading}
          API_URL={API_URL}
          lastShopElementRef={lastShopElementRef}
        />
        
        {loadingMore && (
          <div className="flex justify-center p-4">
            <div className="loader text-center">
              <div className="animate-pulse">Loading more shops...</div>
            </div>
          </div>
        )}
        
        {!hasMore && filteredShops.length > 0 && (
          <div className="text-center p-4 text-gray-500">
            No more coffee shops to load
          </div>
        )}
      </main>
      <Footer index={1} />
    </div>
  );
}