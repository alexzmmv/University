import Link from 'next/link';

export const Header = ({ page }) => {
    return (
        <header className="relative w-full h-[90px] bg-[#FDF8F5] border-b border-[#E5E7EB]">
            <div className="h-[30px] border-b border-[#E5E7EB]"></div>
            <div className="flex items-center h-[60px]">
                <Link href={page || '/'} className="ml-4 w-[33px] h-[20px] flex items-center justify-center cursor-pointer">
                    <svg width="17.5" height="20" viewBox="0 0 17.5 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M0.367188 9.11719C-0.121094 9.60547 -0.121094 10.3984 0.367188 10.8867L6.61719 17.1367C7.10547 17.625 7.89844 17.625 8.38672 17.1367C8.875 16.6484 8.875 15.8555 8.38672 15.3672L4.26562 11.25H16.25C16.9414 11.25 17.5 10.6914 17.5 10C17.5 9.30859 16.9414 8.75 16.25 8.75H4.26953L8.38281 4.63281C8.87109 4.14453 8.87109 3.35156 8.38281 2.86328C7.89453 2.375 7.10156 2.375 6.61328 2.86328L0.363281 9.11328L0.367188 9.11719Z" fill="#4A3428"/>
                    </svg>
                </Link>
                
                <div className="flex-1 text-center">
                    <h1 className="text-lg font-medium text-[#4A3428]">EXPLORE</h1>
                </div>
                
                <div className="w-[33px]"></div>
            </div>
        </header>
    );
};