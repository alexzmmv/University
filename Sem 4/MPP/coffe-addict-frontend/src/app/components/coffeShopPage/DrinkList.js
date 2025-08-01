import { useState } from "react";
import { DrinkCard } from '@/app/components/coffeShopPage/DrinkCard';
import { EditDrinkForm } from '@/app/components/coffeShopPage/EditDrinkForm';

export const toggleEditMode = (drinkId, currentEditingId, setEditingId) => {
    if (currentEditingId === drinkId) {
        setEditingId(null);
    } else {
        setEditingId(drinkId);
    }
};


const EmptyState = () => (
    <div className="flex flex-col items-center justify-center h-64 w-full">
        <div className="text-gray-400 text-lg">No drinks available on this list</div>
    </div>
);

export const saveDrinkEdit = (updatedDrink, updateCallback, setEditingId) => {
    updateCallback(updatedDrink);
    setEditingId(null);
};

export const cancelDrinkEdit = (setEditingId) => {
    setEditingId(null);
};

export const deleteDrink = (drinkId, deleteCallback) => {
    deleteCallback(drinkId);
};


export const DrinkList = ({ drinks, onDrinkUpdate, onDrinkDelete }) => {
    const [editingDrinkId, setEditingDrinkId] = useState(null);

    const handleEditClick = (drink) => {
        toggleEditMode(drink.id, editingDrinkId, setEditingDrinkId);
    };

    const handleSaveEdit = (updatedDrink) => {
        saveDrinkEdit(updatedDrink, onDrinkUpdate, setEditingDrinkId);
    };

    const handleCancelEdit = () => {
        cancelDrinkEdit(setEditingDrinkId);
    };

    const handleDeleteDrink = (drinkId) => {
        deleteDrink(drinkId, onDrinkDelete);
    };

    if (drinks.length === 0) {
        return <EmptyState />;
    }

    const prices = drinks.map(drink => drink.price);
    const minPrice = Math.min(...prices);
    const maxPrice = Math.max(...prices);

    return (
        <div className="bg-gray-100 mb-6 w-screen flex justify-center">
            <div className="drink-grid grid grid-cols-1 max-w-4xl w-full">
                {drinks.map((drink) => (
                    editingDrinkId === drink.id ? (
                        <EditDrinkForm 
                            key={drink.id}
                            drink={drink}
                            onSave={handleSaveEdit}
                            onCancel={handleCancelEdit}
                            onDelete={() => handleDeleteDrink(drink.id)} 
                        />
                    ) : (
                        <DrinkCard 
                            key={drink.id}
                            drink={drink}
                            onEdit={handleEditClick}
                            priceColor={drink.color}
                        />
                    )
                ))}
            </div>
        </div>
    );
};