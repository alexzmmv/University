"use client"
import { useState, useEffect, useCallback, useRef } from "react";
import { SearchBar } from "./SearchBar";
import { FilterBar } from "./FilterBar";
import { Sort } from "./Sort"; 
import axios from "axios";

export function SearchFilterSortSection({ allShops, onFilteredResultsChange, userLocation, API_URL, onlineFiltering }) {
  const [searchQuery, setSearchQuery] = useState('');
  const [activeFilters, setActiveFilters] = useState([]);
  const [activeSort, setActiveSort] = useState('rating');
  const [isLoading, setIsLoading] = useState(false);
  
  // Use refs to track changes without triggering re-renders
  const debounceTimerRef = useRef(null);
  const lastRequestParamsRef = useRef('');
  const requestInProgressRef = useRef(false);
  
  // Memoize this function but don't make it trigger rerenders
  const fetchFilteredShops = useCallback(async (forceFetch = false) => {
    if (!allShops || allShops.length === 0) return;
    
    // Build params to check if anything has actually changed
    const params = new URLSearchParams();
    params.append('latitude', userLocation.latitude);
    params.append('longitude', userLocation.longitude);
    if (searchQuery) params.append('search', searchQuery);
    if (activeFilters.includes('openNow')) params.append('Open', true);
    if (activeFilters.includes('nearby')) params.append('max_distance', 1);
    if (activeFilters.includes('highRated')) params.append('min_rating', 4.5);
    
    if (activeSort === 'rating' || activeSort === 'distance') {
      params.append('sort_by', activeSort === 'rating' ? 'rating' : 'location');
      params.append('sort_order', activeSort === 'rating' ? 'desc' : 'asc');
    }
    
    const paramsString = params.toString();
    
    // Skip if nothing changed and not forced
    if (!forceFetch && paramsString === lastRequestParamsRef.current) {
      return;
    }
    
    // Skip if there's already a request in progress
    if (requestInProgressRef.current && !forceFetch) {
      return;
    }
    
    lastRequestParamsRef.current = paramsString;
    
    let filtered = [...allShops];
    
    if (onlineFiltering) {
      setIsLoading(true);
      requestInProgressRef.current = true;
      
      // Create new URLSearchParams object
      const params = new URLSearchParams();
      
      // Add required parameters
      params.append('latitude', userLocation.latitude);
      params.append('longitude', userLocation.longitude);
      
      // Add optional filter parameters only if they're set
      if (searchQuery) params.append('search', searchQuery);
      if (activeFilters.includes('openNow')) params.append('Open', 'true');
      if (activeFilters.includes('nearby')) params.append('max_distance', '1');
      if (activeFilters.includes('highRated')) params.append('min_rating', '4.5');
      
      // Set sorting parameters
      if (activeSort === 'rating') {
        params.append('sort_by', 'rating');
        params.append('sort_order', 'desc');
      } else if (activeSort === 'distance') {
        params.append('sort_by', 'location');
        params.append('sort_order', 'asc');
      }
      
      // Add pagination parameters
      params.append('page', '1');
      params.append('page_size', '50');
      
      try {
        console.log("Fetching filtered shops with params:", params.toString());
        
        // Fix: Ensure the URL doesn't have double slashes by checking API_URL format
        const baseUrl = API_URL.endsWith('/') ? API_URL.slice(0, -1) : API_URL;
        const response = await axios.get(`${baseUrl}/coffee-shops?${params.toString()}`);
        
        if (response.data && response.data.coffee_shops) {
          filtered = response.data.coffee_shops.map(shop => ({
            id: shop.public_id,
            name: shop.name,
            rating: shop.rating.toString(),
            distance: `${shop.distance.toFixed(1)} km`,
            status: shop.status,
            image: shop.image
          }));
          
          const uniqueFiltered = Array.from(
            new Map(filtered.map(shop => [shop.id, shop])).values()
          );
          
          console.log(`Filtered shops from API: ${uniqueFiltered.length}`);
          onFilteredResultsChange(uniqueFiltered);
        }
      } catch (error) {
        console.error('Error fetching filtered coffee shops:', error);
        console.log('Error details:', error.response ? error.response.status : 'No response');
        applyLocalFilters();
      } finally {
        setIsLoading(false);
        requestInProgressRef.current = false;
      }
    } else {
      applyLocalFilters();
    }
  }, [searchQuery, activeFilters, activeSort, allShops, userLocation, API_URL, onlineFiltering]);

  const applyLocalFilters = () => {
    let filtered = [...allShops];
    
    if (searchQuery) {
      filtered = filtered.filter(shop => 
        shop.name.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }
    
    if (activeFilters.includes('openNow')) {
      filtered = filtered.filter(shop => 
        shop.status.toLowerCase().includes('open')
      );
    }
    
    if (activeFilters.includes('nearby')) {
      filtered = filtered.filter(shop => {
        const distanceStr = shop.distance.replace(' km', '');
        const distanceValue = parseFloat(distanceStr);
        return !isNaN(distanceValue) && distanceValue < 1;
      });
    }
    
    if (activeFilters.includes('highRated')) {
      filtered = filtered.filter(shop => parseFloat(shop.rating) >= 4.5);
    }
    
    if (activeSort === 'rating') {
      filtered.sort((a, b) => parseFloat(b.rating) - parseFloat(a.rating));
    } else if (activeSort === 'distance') {
      filtered.sort((a, b) => {
        const distanceA = parseFloat(a.distance.replace(' km', ''));
        const distanceB = parseFloat(b.distance.replace(' km', ''));
        return distanceA - distanceB;
      });
    }
    
    // Ensure consistent distance format for all filtered shops
    filtered = filtered.map(shop => {
      const distanceValue = parseFloat(shop.distance.replace(' km', ''));
      return {
        ...shop,
        distance: `${distanceValue.toFixed(1)} km`
      };
    });
    
    const uniqueFiltered = Array.from(
      new Map(filtered.map(shop => [shop.id, shop])).values()
    );
    
    console.log(`Filtered shops locally: ${uniqueFiltered.length}`);
    onFilteredResultsChange(uniqueFiltered);
  };

  // Use debouncing for all filter changes
  const debouncedFetchShops = (forceFetch = false) => {
    if (debounceTimerRef.current) {
      clearTimeout(debounceTimerRef.current);
    }
    
    debounceTimerRef.current = setTimeout(() => {
      fetchFilteredShops(forceFetch);
    }, 500); // Increased debounce time to 500ms
  };

  // Only fetch when component mounts or when location changes
  useEffect(() => {
    fetchFilteredShops(true); // Force fetch on initial load
    
    return () => {
      if (debounceTimerRef.current) {
        clearTimeout(debounceTimerRef.current);
      }
    };
  }, [userLocation]); // Only dependent on location changes

  // Use separate effect for filter changes with proper debouncing
  useEffect(() => {
    debouncedFetchShops();
    return () => {
      if (debounceTimerRef.current) {
        clearTimeout(debounceTimerRef.current);
      }
    };
  }, [searchQuery, activeFilters, activeSort]);

  const handleSearchChange = (newQuery) => {
    setSearchQuery(newQuery);
  };

  const handleFilterChange = (newFilters) => {
    setActiveFilters(newFilters);
  };

  const handleSortChange = (newSort) => {
    setActiveSort(newSort);
  };

  return (
    <div className="mb-6">
      <SearchBar 
        searchQuery={searchQuery} 
        onSearchChange={handleSearchChange} 
      />
      <FilterBar 
        activeFilters={activeFilters} 
        onFilterChange={handleFilterChange} 
      />
      <Sort 
        activeSort={activeSort} 
        onSortChange={handleSortChange} 
      />
      {isLoading && (
        <div className="flex justify-center my-2">
          <div className="text-sm text-gray-500">Updating results...</div>
        </div>
      )}
    </div>
  );
}