import Image from 'next/image';
import starIcon from "../../resources/coffeShopCard/star.svg";
import saveIcon from "../../resources/coffeShopCard/save.svg";

export const CoffeeShopCard = ({ name, rating, distance, status, image, onTap}) => {
  return (
    <div className="flex flex-col w-[95%] mx-auto max-w-md h-auto bg-white rounded-2xl p-4 relative shadow-md" onClick={() => onTap()}>
      <div className="flex items-start">
        <div
          className="w-16 h-16 rounded-xl bg-cover bg-center flex-shrink-0"
          style={{ backgroundImage: `url(${image})` }}
        />
        <div className="ml-4 flex flex-col justify-between flex-grow">
          <div className="font-bold text-[#4a3428] text-base leading-5">
            {name}
          </div>
          <div className="flex items-center text-sm text-[#8b7355] mt-1">
            <Image width={16} height={14} className="w-4 h-4 mr-1" alt="Rating Icon" src={starIcon} />
            <span>{rating}</span>
            <span className="mx-2">•</span>
            <span>{distance} km</span>
          </div>
        </div>
      </div>

      <div className="mt-2 text-sm text-[#8b7355]">{status}</div>

      <div className="absolute top-2 right-4">
        <Image width={12} height={16} className="w-4 h-4" alt="Frame Icon" src={saveIcon} />
      </div>
    </div>
  );
};