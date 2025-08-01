'use client';

import Link from 'next/link';
import { useAuth } from '../../utils/AuthContext';
import { useRouter } from 'next/navigation';

// Header Component
export const Header = () => {
  const { user, logout, isAuthenticated } = useAuth();
  const router = useRouter();

  const handleLogout = () => {
    logout();
    router.push('/auth/login');
  };

  return (
    <header className="p-4 bg-[#fdf8f5] shadow-md">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-[#4a3428]">Coffee Addict</h1>
          <p className="text-sm text-[#8b7355]">Find your perfect brew</p>
        </div>
        <div className="flex items-center">
          {isAuthenticated ? (
            <>
              <span className="mr-4 text-[#4a3428] font-medium">Hi, {user?.username}</span>
            </>
          ) : (
            <>
              <Link 
                href="/auth/login" 
                className="px-4 py-2 rounded-full text-sm font-medium text-white bg-[#6f4e37] hover:bg-[#5d4130] transition-colors duration-200 mr-3 shadow-sm"
              >
                Login
              </Link>
              <Link 
                href="/auth/register" 
                className="px-4 py-2 rounded-full text-sm font-medium text-[#6f4e37] bg-[#4a9b79] hover:bg-[#3b8a6a] transition-colors duration-200 shadow-sm"
              >
                Register
              </Link>
            </>
          )}
        </div>
      </div>
    </header>
  );
};