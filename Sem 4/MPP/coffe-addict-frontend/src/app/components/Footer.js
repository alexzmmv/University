"use client"
import Image from 'next/image';
import homeActive from "../resources/barIcons/active/home.svg";
import homeInactive from "../resources/barIcons/inactive/home.svg"
import originsInactive from "../resources/barIcons/inactive/origins.svg";
import originsActive from "../resources/barIcons/active/origins.svg"
import brewInactive from "../resources/barIcons/inactive/brew.svg";
import brewActive from "../resources/barIcons/active/brew.svg"; // Added this if available
import profileInactive from "../resources/barIcons/inactive/profile.svg";
import profileActive from "../resources/barIcons/active/profile.svg";

const FooterButton = ({ icon, label, isActive, onClickAction}) => {
    return (
        <button 
            className="all-[unset] flex flex-col items-center justify-center w-10 h-10 rounded-full transition-all duration-200 hover:bg-[#f0e8e0] hover:scale-110" 
            onClick={onClickAction}
        >
            <Image width={20} height={20} className="w-5 h-5" alt={label} src={icon} />
            <div
                className={`text-xs font-normal ${
                    isActive ? "text-[#4a3428]" : "text-[#8b7355]"
                }`}
            >
                {label}
            </div>
        </button>
    );
};

export const Footer = ({ index}) => {

    return (
        <div className="fixed bottom-0 left-0 w-full h-[73px] bg-white border-t border-[#e8e0db] shadow-md flex justify-around items-center">
            <FooterButton
                onClickAction={index===1?()=>{}:()=>{window.location.href = '/'}} 
                icon={index === 1 ? homeActive : homeInactive}
                label="Home"
                isActive={index === 1}
            />
            <FooterButton
                onClickAction={index===2?()=>{}:()=>{}} 
                icon={index === 2 ? originsActive : originsInactive}
                label="Origins"
                isActive={index === 2}
            />
            <FooterButton
                onClickAction={index===3?()=>{}:()=>{window.location.href = '/mybrews'}} 
                icon={index === 3 ? brewActive : brewInactive}
                label="MyBrews"
                isActive={index === 3}
            />
            <FooterButton
                onClickAction={index===4?()=>{}:()=>{window.location.href = '/auth/profile'}} 
                icon={index === 4 ? profileActive : profileInactive}
                label="Profile"
                isActive={index === 4}
            />
        </div>
    );
};
