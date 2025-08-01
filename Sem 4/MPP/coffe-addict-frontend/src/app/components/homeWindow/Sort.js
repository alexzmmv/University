"use client"

export function Sort({ activeSort, onSortChange }) {
    const sortOptions = [
        { id: 'rating', label: 'Highest Rated' },
        { id: 'distance', label: 'Nearest First' },
    ];
    
    return (
        <div className="flex items-center mb-4">
            <span className="mr-2 text-gray-700">Sort by:</span>
            <div className="flex flex-wrap gap-2">
                {sortOptions.map((option) => (
                    <button
                        key={option.id}
                        className={`px-4 py-1 rounded-full ${
                            activeSort === option.id
                                ? 'bg-amber-800 text-white'
                                : 'bg-gray-200 text-gray-800'
                        }`}
                        onClick={() => onSortChange(option.id)}
                    >
                        {option.label}
                    </button>
                ))}
            </div>
        </div>
    );
}