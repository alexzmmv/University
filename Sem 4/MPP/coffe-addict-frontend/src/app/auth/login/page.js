'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useAuth } from '../../utils/AuthContext';
import { Header } from '../../components/homeWindow/Header';
import { Footer } from '../../components/Footer';

export default function Login() {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  });
  const [isLoading, setIsLoading] = useState(false);
  const [formError, setFormError] = useState('');
  const { login, error, isAuthenticated } = useAuth();
  const router = useRouter();

  // Redirect if already authenticated
  useEffect(() => {
    if (isAuthenticated) {
      router.push('/');
    }
  }, [isAuthenticated, router]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
    // Clear form error when user types
    setFormError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Basic form validation
    if (!formData.username.trim()) {
      setFormError('Username is required');
      return;
    }
    
    if (!formData.password) {
      setFormError('Password is required');
      return;
    }
    
    setIsLoading(true);
    setFormError(''); // Clear any previous errors
    
    try {
      const result = await login(formData.username, formData.password);
      
      // Debug: Log the result to see what we're getting
      console.log('Login result:', result);
      
      if (result.requires2FA) {
        // Show brief success message before redirect
        console.log('2FA required, redirecting to verify-2fa page');
        setFormError('');
        // Redirect to 2FA verification page with necessary data
        const params = new URLSearchParams({
          jobId: result.jobId,
          phoneHint: result.phoneHint,
          message: result.message
        });
        console.log('2FA params:', params.toString());
        router.push(`/auth/verify-2fa?${params.toString()}`);
        return; // Don't set loading to false immediately for smoother transition
      } else if (result.success) {
        console.log('Login successful without 2FA');
        setFormError('');
        router.push('/');
        return; // Don't set loading to false immediately for smoother transition
      } else {
        console.log('Login failed:', result.error);
        setFormError(result.error || 'Login failed');
      }
    } catch (err) {
      console.error('Login error:', err);
      setFormError('Login failed. Please try again.');
    } finally {
      // Only set loading to false if we're not redirecting
      setTimeout(() => setIsLoading(false), 100);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-[#fdf8f5]">
      <Header />
      <div className="flex-grow flex items-center justify-center pb-20">
        <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md border border-[#e8e0db] mx-4">
          <h1 className="text-2xl font-bold mb-6 text-center text-[#4a3428]">Login to Coffee Addict</h1>
          
          {(error || formError) && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4" role="alert">
              <span className="block sm:inline">{formError || error}</span>
            </div>
          )}
        
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label htmlFor="username" className="block text-[#4a3428] text-sm font-bold mb-2">
              Username
            </label>
            <input
              type="text"
              id="username"
              name="username"
              value={formData.username}
              onChange={handleChange}
              className="shadow-sm appearance-none border border-[#e8e0db] rounded-md w-full py-2 px-3 text-[#4a3428] leading-tight focus:outline-none focus:ring-2 focus:ring-[#6f4e37] focus:border-transparent transition-colors duration-200"
              required
            />
          </div>
          
          <div className="mb-6">
            <label htmlFor="password" className="block text-[#4a3428] text-sm font-bold mb-2">
              Password
            </label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              className="shadow-sm appearance-none border border-[#e8e0db] rounded-md w-full py-2 px-3 text-[#4a3428] leading-tight focus:outline-none focus:ring-2 focus:ring-[#6f4e37] focus:border-transparent transition-colors duration-200"
              required
            />
          </div>
          
          <div className="flex items-center justify-between">
            <button
              type="submit"
              className="bg-[#6f4e37] hover:bg-[#5d4130] text-white font-medium py-2 px-4 rounded-full focus:outline-none focus:shadow-outline w-full transition-colors duration-200 shadow-sm"
              disabled={isLoading}
            >
              {isLoading ? 'Logging in...' : 'Login'}
            </button>
          </div>
        </form>
        
        <div className="mt-6 text-center">
          <p className="text-[#8b7355]">
            Don't have an account?{' '}
            <Link href="/auth/register" className="text-[#6f4e37] hover:text-[#5d4130] font-medium transition-colors duration-200">
              Register
            </Link>
          </p>
        </div>
      </div>
      </div>
      <Footer index={4} />
    </div>
  );
}
