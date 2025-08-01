export const DrinkCard = ({ drink, onEdit, priceColor = "#311D09" }) => {
    const { name, description, price, image } = drink;
    
    return (
        <div 
            className="flex w-full max-w h-auto bg-[#F9F5F1] rounded-3xl p-5 relative shadow-sm  hover:shadow-md transition-shadow" 
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
                    <span className="text-xl font-bold" style={{ color: priceColor }}>${price}</span>
                    <button 
                        className="bg-[#C94C10] text-white text-sm px-4 py-2 rounded-full hover:bg-[#B33E08] transition-colors" 
                        onClick={() => onEdit(drink)}
                    >
                        Edit
                    </button>
                </div>
            </div>
        </div>
    );
}
