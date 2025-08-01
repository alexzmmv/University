'use client';

import { useAuth } from '../../utils/AuthContext';
import { useRouter } from 'next/navigation';
import { Footer } from '../../components/Footer';
import { Header } from '../../components/homeWindow/Header';

export default function Profile() {
  const { user, logout } = useAuth();
  const router = useRouter();

  const handleLogout = () => {
    logout();
    router.push('/auth/login');
  };

  if (!user) {
    return (
      <div className="min-h-screen flex flex-col bg-[#fdf8f5]">
        <Header />
        <div className="flex-grow flex items-center justify-center pb-20">
          <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md text-center border border-[#e8e0db] mx-4">
            <p className="mb-4 text-[#4a3428]">You are not logged in.</p>
            <button
              onClick={() => router.push('/auth/login')}
              className="bg-[#6f4e37] hover:bg-[#5d4130] text-white font-medium py-2 px-4 rounded-full focus:outline-none transition-colors duration-200 shadow-sm"
            >
              Log In
            </button>
          </div>
        </div>
        <Footer index={4} />
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col bg-[#fdf8f5]">
      <Header />
      <div className="flex-grow py-12 px-4 sm:px-6 lg:px-8 pb-20">
        <div className="max-w-md mx-auto bg-white rounded-lg shadow-md overflow-hidden border border-[#e8e0db]">
          <div className="bg-[#6f4e37] text-white px-6 py-4">
            <h1 className="text-2xl font-bold">Profile</h1>
          </div>
          
          <div className="p-6">
            <div className="mb-6">
              <h2 className="text-xl font-semibold mb-4 text-[#4a3428]">User Information</h2>
              <div className="space-y-3">
                <div>
                  <span className="font-medium text-[#4a3428]">Username:</span> <span className="text-[#8b7355]">{user.username}</span>
                </div>
                <div>
                  <span className="font-medium text-[#4a3428]">Email:</span> <span className="text-[#8b7355]">{user.email}</span>
                </div>
                <div>
                  <span className="font-medium text-[#4a3428]">Phone Number:</span> <span className="text-[#8b7355]">{user.phone_number}</span>
                </div>
                <div>
                  <span className="font-medium text-[#4a3428]">Two-Factor Authentication:</span>{' '}
                  <span className={`text-sm font-medium px-2 py-1 rounded-full ${user.enable_2fa ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                    {user.enable_2fa ? 'Enabled' : 'Disabled'}
                  </span>
                </div>
                <div>
                  <span className="font-medium text-[#4a3428]">Account created:</span>{' '}
                  <span className="text-[#8b7355]">{new Date(user.created_at).toLocaleDateString()}</span>
                </div>
              </div>
            </div>
            
            <div className="flex justify-center">
              <button
                onClick={handleLogout}
                className="px-4 py-2 rounded-full text-sm font-medium text-white bg-[#c04a4a] hover:bg-[#a83c3c] transition-colors duration-200 shadow-sm"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </div>
      <Footer index={4} />
    </div>
  );
}
