import Image from "next/image";
import searchIcon from "../../resources/search.svg"

export function SearchBar({ searchQuery, onSearchChange }) {
  return (
    <div className="mb-4 relative">
      <div className="relative flex items-center">
        <div className="absolute left-2 flex items-center pointer-events-none">
          <Image src={searchIcon} alt="Search" width={20} height={20}/>
        </div>
        <input
          type="text"
          placeholder="Search coffee shops..."
          value={searchQuery}
          onChange={(e) => onSearchChange(e.target.value)}
          className="w-full p-3 pl-10 bg-white border border-[#E5E7EB] rounded-full focus:outline-none focus:ring-2 focus:ring-brown-500 text-[#ADAEBC] shadow-sm"
        />
      </div>
    </div>
  );
}