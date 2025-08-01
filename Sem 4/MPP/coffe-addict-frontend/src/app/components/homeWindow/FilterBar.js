"use client"

export function FilterBar({ activeFilters, onFilterChange }) {
  const filterOptions = [
    { id: 'openNow', label: 'Open Now' },
    { id: 'highRated', label: '4.5+' },
    { id: 'nearby', label: 'Within 1 km' },
  ];
  
  const toggleFilter = (filterId) => {
    onFilterChange(prev => 
      prev.includes(filterId)
        ? prev.filter(id => id !== filterId)
        : [...prev, filterId]
    );
  };

  return (
    <div className="flex flex-wrap gap-2 mb-4">
      {filterOptions.map((option) => (
        <button
          key={option.id}
          className={`px-4 py-1 rounded-full ${
            activeFilters.includes(option.id)
              ? 'bg-amber-800 text-white'
              : 'bg-gray-200 text-gray-800'
          }`}
          onClick={() => toggleFilter(option.id)}
        >
          {option.label}
        </button>
      ))}
    </div>
  );
}