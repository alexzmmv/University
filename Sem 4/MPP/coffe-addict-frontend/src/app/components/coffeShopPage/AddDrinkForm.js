import { useState } from "react";

export const AddDrinkForm = ({ onAdd, onCancel }) => {
    const [newDrink, setNewDrink] = useState({
        name: '',
        description: '',
        price: '',
        image: 'https://picsum.photos/seed/NewDrink/200/200',
        sales: 100,
        popularity: 100
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        if (name === 'price' && value > 0 || name !== 'price') {
            setNewDrink(prev => ({
                ...prev,
                [name]: value
            }));
        }
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!newDrink.name || !newDrink.description || !newDrink.price || !newDrink.sales || !newDrink.popularity) {
            alert('Please fill in all fields');
            return;
        }
        onAdd({
            ...newDrink,
            price: Number(newDrink.price).toFixed(2)
        });
        setNewDrink({
            name: '',
            description: '',
            price: '',
            image: 'https://picsum.photos/seed/NewDrink/200/200',
            sales: 100,
            popularity: 100
        });
    };

    const { name, description, price, image, sales, popularity } = newDrink;
    
    return (
        <div 
            className="flex mb-6 max-w-4xl w-full max-w h-auto bg-[#F9F5F1] rounded-3xl p-5 relative shadow-sm cursor-pointer hover:shadow-md transition-shadow"
        >
            <img 
                className="w-[5.5em] h-[5.5em] rounded-2xl object-cover flex-shrink-0 mr-4" 
                src={image} 
                alt="New drink"
                width={88}
                height={88}
            />
            <div className="flex p-5 flex-col justify-between flex-grow">
                <input
                    type="text"
                    name="name"
                    placeholder="Drink name"
                    value={name}
                    onChange={handleChange}
                    className="font-semibold text-[#311D09] text-lg leading-6 bg-transparent border-b border-[#7E7162] focus:outline-none"
                    required
                />
                <textarea
                    name="description"
                    placeholder="Description"
                    value={description}
                    onChange={handleChange}
                    className="text-sm text-[#7E7162] mt-1 bg-transparent border-b border-[#7E7162] focus:outline-none resize-none min-h-[2.5em]"
                    required
                ></textarea>
                <div className="flex justify-between items-center mt-2">
                    <div className="flex items-center">
                        <span className="text-xl font-bold text-[#311D09] mr-1">$</span>
                        <input
                            type="number"
                            name="price"
                            placeholder="0.00"
                            value={price}
                            onChange={handleChange}
                            className="w-16 text-xl font-bold text-[#311D09] bg-transparent border-b border-[#7E7162] focus:outline-none"
                            min="0.01"
                            step="0.01"
                            required
                        />
                    </div>
                    <div className="flex items-center">
                        <span className="text-sm text-[#7E7162] mr-1">Sales:</span>
                        <input
                            type="number"
                            name="sales"
                            value={sales}
                            onChange={handleChange}
                            className="w-16 text-sm text-[#311D09] bg-transparent border-b border-[#7E7162] focus:outline-none"
                            min="0"
                            required
                        />
                    </div>
                    <div className="flex items-center">
                        <span className="text-sm text-[#7E7162] mr-1">Popularity:</span>
                        <input
                            type="number"
                            name="popularity"
                            value={popularity}
                            onChange={handleChange}
                            className="w-16 text-sm text-[#311D09] bg-transparent border-b border-[#7E7162] focus:outline-none"
                            min="0" 
                            max="100"
                            required
                        />
                    </div>
                </div>
                <div className="flex justify-end items-center mt-2 pt-2">
                    <div className="flex gap-2">
                        <button 
                            type="button"
                            onClick={onCancel}
                            className="bg-[#E5DED5] text-[#7E7162] text-sm px-4 py-2 rounded-full hover:bg-[#D9CFC4] transition-colors"
                        >
                            Cancel
                        </button>
                        <button 
                            onClick={handleSubmit}
                            className="bg-[#C94C10] text-white text-sm px-4 py-2 rounded-full hover:bg-[#B33E08] transition-colors"
                        >
                            Add Drink
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}