"use client"
import { useState } from 'react';


const DrinkCard = ({ drink, onPress, onEdit, onDelete}) => {
    const { name, description, price, image } = drink;

    return (
        <div 
            className="flex w-full max-w-lg h-auto bg-[#F9F5F1] rounded-3xl p-5 relative shadow-sm cursor-pointer hover:shadow-md transition-shadow" 
            onClick={() => onPress(drink)}
        >
            <img 
                className="w-[5.5em] h-[5.5em] rounded-2xl object-cover flex-shrink-0 mr-4" 
                src={image} 
                alt={name}
                width={88}
                height={88}
            />
            <div className="flex flex-col justify-between flex-grow">
                <div className="font-semibold text-[#311D09] text-lg leading-6">
                    {name}
                </div>
                <p className="text-sm text-[#7E7162] mt-1 line-clamp-2">
                    {description}
                </p>
                <div className="flex justify-between items-center mt-auto pt-2">
                    <span className="text-xl font-bold text-[#311D09]">${price}</span>
                    <button 
                        className="bg-[#C94C10] text-white text-sm px-4 py-2 rounded-full hover:bg-[#B33E08] transition-colors" 
                        onClick={(e) => {
                            onEdit(drink); 
                        }}
                    >
                        + Edit
                    </button>
                </div>
            </div>
        </div>
    );
};

const DrinkList = ({ drinks = [], onDrinkUpdate }) => {
    const [editingDrink, setEditingDrink] = useState(null);
    const [editFormData, setEditFormData] = useState({
        name: '',
        description: '',
        price: ''
    });

    const handleEditClick = (drink) => {
        setEditingDrink(drink.id !== undefined ? drink.id : drink._id);
        setEditFormData({
            name: drink.name,
            description: drink.description,
            price: drink.price
        });
    };

    const handleCancelEdit = () => {
        setEditingDrink(null);
    };

    const handleSaveEdit = () => {
        if (onDrinkUpdate) {
            const originalDrink = drinks.find(d => 
                (d.id !== undefined ? d.id : d._id) === editingDrink
            );
            
            if (originalDrink) {
                const updatedDrink = {
                    ...originalDrink,
                    name: editFormData.name,
                    description: editFormData.description,
                    price: Number(editFormData.price)
                };
                onDrinkUpdate(updatedDrink);
            }
        }
        setEditingDrink(null);
    };

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setEditFormData({
            ...editFormData,
            [name]: value
        });
    };

    return (
        <div className="bg-gray-100 mb-6">
            <div className="drink-grid grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                {drinks.length > 0 ? (
                    drinks.map((drink, index) => {
                        const drinkId = drink.id;
                        const isEditing = editingDrink === drinkId;
                        
                        if (isEditing) {
                            return (
                                <div key={drinkId} className="bg-white rounded-lg shadow-md overflow-hidden">
                                    <div className="p-4">
                                        <form onSubmit={(e) => {
                                            e.preventDefault();
                                            handleSaveEdit();
                                        }}>
                                            <input
                                                type="text"
                                                name="name"
                                                value={editFormData.name}
                                                onChange={handleInputChange}
                                                className="w-full p-2 mb-2 border rounded-lg text-sm"
                                                required
                                            />
                                            
                                            <textarea
                                                name="description"
                                                value={editFormData.description}
                                                onChange={handleInputChange}
                                                className="w-full p-2 mb-2 border rounded-lg text-sm"
                                                rows="3"
                                                required
                                            />
                                            
                                            <input
                                                type="number"
                                                name="price"
                                                value={editFormData.price}
                                                onChange={handleInputChange}
                                                className="w-full p-2 mb-3 border rounded-lg text-sm"
                                                step="0.01"
                                                required
                                            />
                                            
                                            <div className="flex justify-between">
                                                <button 
                                                    type="button" 
                                                    onClick={handleCancelEdit}
                                                    className="bg-gray-300 text-gray-800 px-4 py-2 rounded-full"
                                                >
                                                    Cancel
                                                </button>
                                                <button 
                                                    type="submit"
                                                    className="bg-green-500 text-white px-4 py-2 rounded-full"
                                                >
                                                    Save
                                                </button>
                                            </div>
                                        </form>
                                    </div>
                                </div>
                            );
                        }
                        
                        return (
                            <DrinkCard 
                                key={drinkId} 
                                drink={drink} 
                                onEdit={handleEditClick}
                            />
                        );
                    })
                ) : (
                    <div className="no-drinks-message flex flex-col items-center justify-center text-center text-gray-600 col-span-full">
                        <svg 
                            className="empty-cup-icon w-16 h-16 text-gray-400 mb-4" 
                            xmlns="http://www.w3.org/2000/svg" 
                            fill="currentColor" 
                            viewBox="0 0 24 24"
                            aria-hidden="true"
                        >
                            <path d="M20,3H4v10c0,2.21 1.79,4 4,4h6c2.21,0 4,-1.79 4,-4v-3h2c1.11,0 2,-0.9 2,-2V5C22,3.89 21.11,3 20,3zM20,8h-2V5h2V8z" />
                        </svg>
                        <p className="text-lg">No drinks available at the moment</p>
                    </div>
                )}
            </div>
        </div>
    );
};
