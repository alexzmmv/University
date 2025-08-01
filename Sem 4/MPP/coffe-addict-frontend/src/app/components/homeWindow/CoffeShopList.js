"use client"
import { useState } from "react";
import { CoffeeShopCard } from "./CoffeeShopCard";

export function CoffeeShopList({ shops, isLoading, lastShopElementRef, API_URL }) {
  const [selectedShop, setSelectedShop] = useState(null);

  const handleShopSelect = (shopId) => {
    setSelectedShop(shopId);
  };

  if (isLoading && shops.length === 0) {
    return (
      <div className="mt-8 flex justify-center">
        <div className="animate-pulse text-center">
          <p className="text-gray-500">Loading coffee shops...</p>
        </div>
      </div>
    );
  }

  if (shops.length === 0) {
    return (
      <div className="mt-8 text-center">
        <p className="text-gray-500">No coffee shops found. Try adjusting your search or filters.</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 gap-4">
      {shops.map((shop, index) => {
        // Only attach the intersection observer ref to the last element
        const isLastElement = index === shops.length - 1;
        
        return (
          <div 
            ref={isLastElement ? lastShopElementRef : null}
            key={shop.id || index}
            className="coffee-shop-card-container"
          >
            <CoffeeShopCard
              name={shop.name}
              rating={shop.rating}
              distance={shop.distance}
              status={shop.status}
              image={shop.image}
              onTap={() => {
                window.location.href = `/coffeshop/${shop.id}`;
              }}
            />
          </div>
        );
      })}
    </div>
  );
}