"use client"
import { useState, useEffect } from 'react';

export const ConnectionStatus = ({ isServerReachable: initialServerStatus }) => {
    const [isOnline, setIsOnline] = useState(true);
    const [isServerReachable, setIsServerReachable] = useState(initialServerStatus);
    const [isMounted, setIsMounted] = useState(false);
    
    useEffect(() => {
        // Once component is mounted on client, we can safely access browser APIs
        setIsMounted(true);
        setIsOnline(navigator.onLine);
        setIsServerReachable(initialServerStatus);
        
        const handleOnlineStatus = () => {
            setIsOnline(navigator.onLine);
        };
        
        window.addEventListener('online', handleOnlineStatus);
        window.addEventListener('offline', handleOnlineStatus);
        
        return () => {
            window.removeEventListener('online', handleOnlineStatus);
            window.removeEventListener('offline', handleOnlineStatus);
        };
    }, [initialServerStatus]);
    
    // Don't render anything during SSR or before client hydration
    if (!isMounted) {
        return null;
    }
    
    return (
        <div className="fixed top-2 right-2 flex gap-2">
            <div className={`px-3 py-1 rounded-full text-xs ${isOnline ? 'bg-green-500 text-white' : 'bg-red-500 text-white'}`}>
                {isOnline ? 'Online' : 'Offline'}
            </div>
            <div className={`px-3 py-1 rounded-full text-xs ${isServerReachable ? 'bg-green-500 text-white' : 'bg-yellow-500 text-white'}`}>
                {isServerReachable ? 'Server OK' : 'Server Down'}
            </div>
        </div>
    );
};
