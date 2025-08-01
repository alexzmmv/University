'use client'
import { useState, useEffect } from 'react';
import { Footer } from "@/app/components/Footer";
import { PlusSignButton } from '@/app/components/PlusSignButton';
import { AddDrinkForm } from '@/app/components/coffeShopPage/AddDrinkForm';
import { DrinkList } from '@/app/components/coffeShopPage/DrinkList';
import { MyCharts } from '@/app/components/coffeShopPage/MyCharts';
import { useParams } from 'next/navigation';
import { ConnectionStatus } from '@/app/components/ConnectionStatus';
import axios from 'axios';
import getConfig from 'next/config';

// Get runtime config
const { publicRuntimeConfig } = getConfig() || {};

// Use environment variable with fallback to config or direct fallback
const API_URL = process.env.API_BASE_URL || (publicRuntimeConfig && publicRuntimeConfig.API_BASE_URL) || "http://localhost:8000/";

// Local storage keys
const PENDING_OPERATIONS_KEY = 'pendingOperations';
const DRINKS_CACHE_KEY = 'drinksCache';

export const addDrink = (drinks, newDrink) => {
    const newDrinkWithId = {
        ...newDrink,
    };
    return [...drinks, newDrinkWithId];
};

export const updateDrink = (drinks, updatedDrink) => {
    return drinks.map(drink => 
        String(drink.id) === String(updatedDrink.id) ? updatedDrink : drink
    );
};

export const deleteDrink = (drinks, drinkId) => {
    return drinks.filter(drink => drink.id !== drinkId);
};

const EmptyState = () => (
    <div className="flex flex-col items-center justify-center h-64 w-full">
        <div className="text-gray-600 mt-4">No drinks available</div>
        <div className="text-gray-600 mt-2">Add a new drink to get started!</div>
    </div>
);

const LoadingState = () => (
    <div className="flex flex-col items-center justify-center h-64 w-full">
        <div className="text-gray-600 mt-4">Loading drinks...</div>
    </div>
);



export default function Page() {
    const [drinks, setDrinks] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showAddForm, setShowAddForm] = useState(false);
    const [currentPage, setCurrentPage] = useState(1);
    const [itemsPerPage] = useState(5);
    const [isOnline, setIsOnline] = useState(navigator.onLine);
    const [isServerReachable, setIsServerReachable] = useState(true);
    const params = useParams();
    const coffeeShopId = params.id;

    const getPendingOperations = () => {
        const storedOperations = localStorage.getItem(PENDING_OPERATIONS_KEY);
        return storedOperations ? JSON.parse(storedOperations) : [];
    };

    const savePendingOperations = (operations) => {
        localStorage.setItem(PENDING_OPERATIONS_KEY, JSON.stringify(operations));
    };

    const clearPendingOperations = () => {
        localStorage.setItem(PENDING_OPERATIONS_KEY, JSON.stringify([]));
    };

    const updateDrinksCache = (drinks) => {
        localStorage.setItem(`${DRINKS_CACHE_KEY}_${coffeeShopId}`, JSON.stringify(drinks));
    };

    const loadCachedDrinks = () => {
        const cachedDrinks = localStorage.getItem(`${DRINKS_CACHE_KEY}_${coffeeShopId}`);
        return cachedDrinks ? JSON.parse(cachedDrinks) : [];
    };

    const checkServerStatus = async () => {
        try {
            await axios.get(`${API_URL}health`, { timeout: 5000 });
            setIsServerReachable(true);
            return true;
        } catch (error) {
            setIsServerReachable(false);
            return false;
        }
    };

    const processPendingOperations = async () => {
        if (!isOnline || !isServerReachable) return;

        let operations = getPendingOperations();
        if (operations.length === 0) return;

        const idMapping = {};
        
        const addOps = operations.filter(op => op.type === 'add');
        let updateOps = operations.filter(op => op.type === 'update');
        let deleteOps = operations.filter(op => op.type === 'delete');
        
        try {
            for (const op of addOps) {
                const tempId = op.data.id || `temp_${Date.now()}`;
                const response = await axios.post(`${API_URL}coffee-shops/${coffeeShopId}/drinks`, op.data);
                
                if (response.data && response.data.id) {
                    idMapping[tempId] = response.data.id;
                }
            }
            
            updateOps = updateOps.map(op => {
                const oldId = op.data.id;
                if (oldId.toString().startsWith('temp_') && idMapping[oldId]) {
                    return {
                        ...op,
                        data: {
                            ...op.data,
                            id: idMapping[oldId]
                        }
                    };
                }
                return op;
            });
            
            updateOps = updateOps.filter(op => {
                const id = op.data.id;
                if (id.toString().startsWith('temp_') && !idMapping[id]) {
                    return false;
                }
                return true;
            });
            deleteOps = deleteOps.map(op => {
                if (op.id.toString().startsWith('temp_') && idMapping[op.id]) {
                    return {
                        ...op,
                        id: idMapping[op.id]
                    };
                }
                return op;
            }).filter(op => {
                const id = op.id;
                if (id.toString().startsWith('temp_') && !idMapping[id]) {
                    return false;
                }
                return true;
            });
            
            for (const op of updateOps) {
                await axios.put(`${API_URL}coffee-shops/${coffeeShopId}/drinks/${op.data.id}`, op.data);
            }
            
            for (const op of deleteOps) {
                await axios.delete(`${API_URL}coffee-shops/${coffeeShopId}/drinks/${op.id}`);
            }
            
            clearPendingOperations();
            await fetchDrinks();
        } catch (error) {
            console.error('Error processing pending operations:', error);
            
            const remainingOperations = [];
            const processedTempIds = Object.keys(idMapping);
            
            operations.forEach(op => {
                if (op.type === 'add') {
                    if (!processedTempIds.includes(op.data.id)) {
                        remainingOperations.push(op);
                    }
                } else if (op.type === 'update') {
                    const id = op.data.id;
                    if (!id.toString().startsWith('temp_') || !processedTempIds.includes(id)) {
                        remainingOperations.push(op);
                    }
                } else if (op.type === 'delete') {
                    const id = op.id;
                    if (!id.toString().startsWith('temp_') || !processedTempIds.includes(id)) {
                        remainingOperations.push(op);
                    }
                }
            });
            
            savePendingOperations(remainingOperations);
        }
    };

    const fetchDrinks = async () => {
        try {
            const serverStatus = await checkServerStatus();
            
            if (!navigator.onLine || !serverStatus) {
                const cachedDrinks = loadCachedDrinks();
                setDrinks(cachedDrinks);
                setLoading(false);
                return;
            }
            
            const response = await axios.get(`${API_URL}coffee-shops/${coffeeShopId}/drinks`);
            const drinks = response.data.drinks || [];

            if (drinks && drinks.length > 0) {
                const prices = drinks.map(drink => parseFloat(drink.price));
                const minPrice = Math.min(...prices);
                const maxPrice = Math.max(...prices);
                
                drinks.forEach(drink => {
                    const price = parseFloat(drink.price);
                    const priceRatio = maxPrice === minPrice ? 0.5 : (price - minPrice) / (maxPrice - minPrice);
                    const red = Math.round(255 * priceRatio);
                    const green = Math.round(255 * (1 - priceRatio));
                    drink.color = `rgb(${red}, ${green}, 0)`;
                });
            }

            setDrinks(drinks);
            updateDrinksCache(drinks);
        } catch (error) {
            console.error('Error fetching drinks:', error);
            setIsServerReachable(false);
            const cachedDrinks = loadCachedDrinks();
            setDrinks(cachedDrinks);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchDrinks();

        const handleOnline = () => {
            setIsOnline(true);
            processPendingOperations();
        };

        const handleOffline = () => {
            setIsOnline(false);
        };

        window.addEventListener('online', handleOnline);
        window.addEventListener('offline', handleOffline);

        const serverCheckInterval = setInterval(() => {
            if (navigator.onLine) {
                checkServerStatus().then(status => {
                    if (status) {
                        processPendingOperations();
                    }
                });
            }
        }, 30000);//30 seconds

        return () => {
            window.removeEventListener('online', handleOnline);
            window.removeEventListener('offline', handleOffline);
            clearInterval(serverCheckInterval);
        };
    }, []);

    const handleUpdateDrink = async (updatedDrink) => {
        if (!isOnline || !isServerReachable) {
            const updatedDrinks = updateDrink(drinks, updatedDrink);
            setDrinks(updatedDrinks);
            updateDrinksCache(updatedDrinks);
            
            const operations = getPendingOperations();
            operations.push({
                type: 'update',
                data: updatedDrink
            });
            savePendingOperations(operations);
            return;
        }

        try {
            await axios.put(`${API_URL}coffee-shops/${coffeeShopId}/drinks/${updatedDrink.id}`, updatedDrink);
            fetchDrinks();
        } catch (error) {
            console.error('Error updating drink:', error);
            setIsServerReachable(false);
            
            const updatedDrinks = updateDrink(drinks, updatedDrink);
            setDrinks(updatedDrinks);
            updateDrinksCache(updatedDrinks);
            
            const operations = getPendingOperations();
            operations.push({
                type: 'update',
                data: updatedDrink
            });
            savePendingOperations(operations);
        }
    };

    const handleAddDrink = async (newDrink) => {
        if (!isOnline || !isServerReachable) {
            const tempId = `temp_${Date.now()}`;
            const drinkWithTempId = { ...newDrink, id: tempId };
            const updatedDrinks = addDrink(drinks, drinkWithTempId);
            setDrinks(updatedDrinks);
            updateDrinksCache(updatedDrinks);
            
            const operations = getPendingOperations();
            operations.push({
                type: 'add',
                data: drinkWithTempId
            });
            savePendingOperations(operations);
            
            setShowAddForm(false);
            return;
        }

        try {
            await axios.post(`${API_URL}coffee-shops/${coffeeShopId}/drinks`, newDrink);
            fetchDrinks();
            setShowAddForm(false);
        } catch (error) {
            console.error('Error adding drink:', error);
            setIsServerReachable(false);
            
            const tempId = `temp_${Date.now()}`;
            const drinkWithTempId = { ...newDrink, id: tempId };
            const updatedDrinks = addDrink(drinks, drinkWithTempId);
            setDrinks(updatedDrinks);
            updateDrinksCache(updatedDrinks);
            
            const operations = getPendingOperations();
            operations.push({
                type: 'add',
                data: drinkWithTempId
            });
            savePendingOperations(operations);
            
            setShowAddForm(false);
        }
    };

    const handleDeleteDrink = async (drinkId) => {
        if (!isOnline || !isServerReachable) {
            const updatedDrinks = deleteDrink(drinks, drinkId);
            setDrinks(updatedDrinks);
            updateDrinksCache(updatedDrinks);
            
            const operations = getPendingOperations();
            
            if (drinkId.toString().startsWith('temp_')) {
                const filteredOperations = operations.filter(op => {
                    if (op.type === 'add' || op.type === 'update') {
                        return op.data.id !== drinkId;
                    } else if (op.type === 'delete') {
                        return op.id !== drinkId;
                    }
                    return true;
                });
                savePendingOperations(filteredOperations);
            } else {
                operations.push({
                    type: 'delete',
                    id: drinkId
                });
                savePendingOperations(operations);
            }
            return;
        }

        try {
            await axios.delete(`${API_URL}coffee-shops/${coffeeShopId}/drinks/${drinkId}`);
            fetchDrinks();
        } catch (error) {
            console.error('Error deleting drink:', error);
            setIsServerReachable(false);
            
            const updatedDrinks = deleteDrink(drinks, drinkId);
            setDrinks(updatedDrinks);
            updateDrinksCache(updatedDrinks);
            
            const operations = getPendingOperations();
            operations.push({
                type: 'delete',
                id: drinkId
            });
            savePendingOperations(operations);
        }
    };

    const indexOfLastItem = currentPage * itemsPerPage;
    const indexOfFirstItem = indexOfLastItem - itemsPerPage;
    const currentDrinks = drinks.slice(indexOfFirstItem, indexOfLastItem);
    const totalPages = Math.ceil(drinks.length / itemsPerPage);

    const handlePageChange = (pageNumber) => {
        setCurrentPage(pageNumber);
    };

    return (
        <div className="flex flex-col items-center justify-center min-h-screen w-full px-4">
            <ConnectionStatus isOnline={isOnline} isServerReachable={isServerReachable} />
            
            {loading ? (
                <LoadingState />
            ) : (
                <>
                    {showAddForm && (
                        <AddDrinkForm 
                            onAdd={handleAddDrink} 
                            onCancel={() => setShowAddForm(false)}
                        />
                    )}
                    {drinks.length === 0 ? (
                        <EmptyState />
                    ) : (
                        <>
                            <DrinkList 
                                drinks={currentDrinks} 
                                onDrinkUpdate={handleUpdateDrink}
                                onDrinkDelete={handleDeleteDrink} 
                            />
                            
                            <div className="flex flex-wrap justify-center align-items-center mt-4 gap-2">
                                <button 
                                    onClick={() => handlePageChange(currentPage - 1)}
                                    disabled={currentPage === 1}
                                    className="px-3 py-1 border rounded disabled:opacity-50"
                                >
                                    Previous
                                </button>
                                
                                <div className="flex gap-1">
                                    {[...Array(totalPages).keys()].map(number => (
                                        <button
                                            key={number + 1}
                                            onClick={() => handlePageChange(number + 1)}
                                            className={`px-3 py-1 border rounded ${
                                                currentPage === number + 1 
                                                ? 'bg-blue-500 text-white' 
                                                : 'hover:bg-gray-100'
                                            }`}
                                        >
                                            {number + 1}
                                        </button>
                                    ))}
                                </div>
                                
                                <button 
                                    onClick={() => handlePageChange(currentPage + 1)}
                                    disabled={currentPage === totalPages}
                                    className="px-3 py-1 border rounded disabled:opacity-50"
                                >
                                    Next
                                </button>
                            </div>
                        </>
                    )}
                </>
            )}
            <MyCharts drinks={drinks}></MyCharts>
            <div className="pb-24"></div>
            <PlusSignButton onTap={() => setShowAddForm(!showAddForm)} />
            <Footer index={1}/>
        </div>
    );
}
