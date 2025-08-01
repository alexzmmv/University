import { useState } from "react";

export const EditDrinkForm = ({ drink, onSave, onCancel, onDelete }) => {
    const [formData, setFormData] = useState({
        id: drink.id,
        name: drink.name,
        description: drink.description,
        price: drink.price,
        image: drink.image,
        sales: drink.sales || 0,
        popularity: drink.popularity || 0

    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        if (name === 'price' && value <= 0) return;
        
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        const stringFormData = Object.keys(formData).reduce((acc, key) => {
            acc[key] = String(formData[key]);
            return acc;
        }, {});
        
        onSave({
            ...drink,
            ...stringFormData,
        });
    };

    const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

    const handleDelete = () => {
        if (showDeleteConfirm) {
            onDelete(drink.id);
        } else {
            setShowDeleteConfirm(true);
        }
    };

    return (
        <div className="flex w-full max-w h-auto bg-[#F9F5F1] rounded-3xl p-3 md:p-5 relative shadow-sm">
            <form onSubmit={handleSubmit} className="flex flex-col w-full gap-2 md:gap-3">
                <div className="flex flex-col md:flex-row">
                    <img 
                        className="w-[12em] h-[12em] md:w-[5.5em] md:h-[5.5em] rounded-2xl object-cover flex-shrink-0 mb-3 md:mb-0 md:mr-4" 
                        src={formData.image} 
                        alt={formData.name}
                        width={88}
                        height={88}
                    />
                    <div className="flex flex-col justify-between flex-grow">
                        <input
                            type="text"
                            name="name"
                            value={formData.name}
                            onChange={handleChange}
                            className="font-semibold text-[#311D09] text-lg leading-6 bg-transparent border-b border-[#7E7162] focus:outline-none"
                            required
                        />
                        <textarea
                            name="description"
                            value={formData.description}
                            onChange={handleChange}
                            className="text-sm text-[#7E7162] mt-1 bg-transparent border-b border-[#7E7162] focus:outline-none resize-none min-h-[2.5em]"
                            required
                        ></textarea>
                        
                        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mt-4 gap-3">
                            <div className="flex flex-wrap gap-3 w-full sm:w-auto">
                                <div className="flex items-center">
                                    <span className="text-xl font-bold text-[#311D09] mr-2">$</span>
                                    <input
                                        type="number"
                                        name="price"
                                        value={formData.price}
                                        onChange={handleChange}
                                        className="w-16 text-xl font-bold text-[#311D09] bg-transparent border-b border-[#7E7162] focus:outline-none"
                                        step="0.01"
                                        min="0.01"
                                        required
                                    />
                                </div>

                                <div className="flex items-center">
                                    <span className="text-sm text-[#7E7162] mr-1">Sales:</span>
                                    <input
                                        type="number"
                                        name="sales"
                                        value={formData.sales || 0}
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
                                        value={formData.popularity || 0}
                                        onChange={handleChange}
                                        className="w-16 text-sm text-[#311D09] bg-transparent border-b border-[#7E7162] focus:outline-none"
                                        min="0" 
                                        max="100"
                                        required
                                    />
                                </div>
                            </div>
                            
                            <div className="flex gap-2 w-full sm:w-auto justify-end">
                                <button 
                                    type="button" 
                                    onClick={onCancel}
                                    className="bg-[#E5DED5] text-[#7E7162] text-sm px-3 py-2 rounded-full hover:bg-[#D9CFC4] transition-colors"
                                >
                                    Cancel
                                </button>
                                <button 
                                    type="button" 
                                    onClick={handleDelete}
                                    className={`${showDeleteConfirm ? 'bg-red-600 text-white' : 'bg-red-400 text-white'} text-sm px-3 py-2 rounded-full hover:bg-red-600 transition-colors`}
                                >
                                    {showDeleteConfirm ? 'Confirm' : 'Delete'}
                                </button>
                                <button 
                                    type="submit"
                                    className="bg-[#C94C10] text-white text-sm px-3 py-2 rounded-full hover:bg-[#B33E08] transition-colors"
                                >
                                    Save
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </form>
        </div>
    );
}