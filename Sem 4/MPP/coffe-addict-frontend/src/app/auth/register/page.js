'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useAuth } from '../../utils/AuthContext';
import { Header } from '../../components/homeWindow/Header';
import { Footer } from '../../components/Footer';

export default function Register() {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    phone_number: '',
    password: '',
    confirmPassword: '',
    enable_2fa: false,
  });
  const [isLoading, setIsLoading] = useState(false);
  const [validationError, setValidationError] = useState(null);
  const { register, error } = useAuth();
  const router = useRouter();

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value,
    });
  };

  const validateForm = () => {
    if (formData.password !== formData.confirmPassword) {
      setValidationError('Passwords do not match');
      return false;
    }
    
    if (formData.password.length < 8) {
      setValidationError('Password must be at least 8 characters long');
      return false;
    }
    
    // Validate phone number (basic validation)
    const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;
    if (!phoneRegex.test(formData.phone_number.replace(/[\s\-\(\)]/g, ''))) {
      setValidationError('Please enter a valid phone number');
      return false;
    }
    
    // If 2FA is enabled, ensure phone number is provided
    if (formData.enable_2fa && !formData.phone_number.trim()) {
      setValidationError('Phone number is required when 2FA is enabled');
      return false;
    }
    
    setValidationError(null);
    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }
    
    setIsLoading(true);
    setValidationError(null); // Clear validation errors
    
    try {
      const result = await register(
        formData.username, 
        formData.email, 
        formData.password, 
        formData.phone_number, 
        formData.enable_2fa
      );
      
      // Debug: Log the result to see what we're getting
      console.log('Registration result:', result);
      
      if (result && result.requires2FA) {
        // Registration successful but 2FA is required for login
        console.log('2FA required, redirecting to verify-2fa page');
        const params = new URLSearchParams({
          jobId: result.jobId,
          phoneHint: result.phoneHint,
          message: result.message || 'Registration successful! Please verify your phone number to complete login.'
        });
        console.log('2FA params:', params.toString());
        router.push(`/auth/verify-2fa?${params.toString()}`);
        return; // Don't set loading to false for smoother transition
      } else if (result && result.success) {
        // Registration and login successful (no 2FA)
        console.log('Registration successful without 2FA');
        setValidationError('');
        router.push('/');
        return; // Don't set loading to false for smoother transition
      } else if (result === false) {
        // Registration failed, error is already set in AuthContext
        console.log('Registration failed');
      }
    } catch (err) {
      console.error('Registration error:', err);
      setValidationError('Registration failed. Please try again.');
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
          <h1 className="text-2xl font-bold mb-6 text-center text-[#4a3428]">Create an Account</h1>
          
          {(error || validationError) && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4" role="alert">
              <span className="block sm:inline">{validationError || error}</span>
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
          
          <div className="mb-4">
            <label htmlFor="email" className="block text-[#4a3428] text-sm font-bold mb-2">
              Email
            </label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              className="shadow-sm appearance-none border border-[#e8e0db] rounded-md w-full py-2 px-3 text-[#4a3428] leading-tight focus:outline-none focus:ring-2 focus:ring-[#6f4e37] focus:border-transparent transition-colors duration-200"
              required
            />
          </div>
          
          <div className="mb-4">
            <label htmlFor="phone_number" className="block text-[#4a3428] text-sm font-bold mb-2">
              Phone Number
            </label>
            <input
              type="tel"
              id="phone_number"
              name="phone_number"
              value={formData.phone_number}
              onChange={handleChange}
              placeholder="+1234567890"
              className="shadow-sm appearance-none border border-[#e8e0db] rounded-md w-full py-2 px-3 text-[#4a3428] leading-tight focus:outline-none focus:ring-2 focus:ring-[#6f4e37] focus:border-transparent transition-colors duration-200"
              required
            />
            <p className="text-xs text-[#8b7355] mt-1">Include country code (e.g., +1 for US numbers)</p>
          </div>
          
          <div className="mb-4">
            <div className="flex items-start">
              <input
                type="checkbox"
                id="enable_2fa"
                name="enable_2fa"
                checked={formData.enable_2fa}
                onChange={handleChange}
                className="mr-3 mt-1 rounded border-[#e8e0db] text-[#6f4e37] focus:ring-[#6f4e37] focus:ring-2"
              />
              <div className="flex-1">
                <label htmlFor="enable_2fa" className="text-[#4a3428] text-sm font-medium cursor-pointer">
                  Enable Two-Factor Authentication (2FA)
                </label>
                <p className="text-xs text-[#8b7355] mt-1">
                  Adds an extra layer of security by sending a verification code to your phone when logging in
                </p>
                {formData.enable_2fa && (
                  <div className="mt-2 p-2 bg-[#e8f5e8] border border-[#4a9b79] rounded-md">
                    <p className="text-xs text-[#4a9b79] font-medium">
                      ✓ Enhanced Security Enabled
                    </p>
                    <p className="text-xs text-[#4a9b79] mt-1">
                      You'll receive an SMS code during login. Make sure your phone number is correct.
                    </p>
                  </div>
                )}
                {!formData.enable_2fa && (
                  <p className="text-xs text-[#8b7355] mt-1 italic">
                    Recommended for better account security
                  </p>
                )}
              </div>
            </div>
          </div>
          
          <div className="mb-4">
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
            <p className="text-xs text-[#8b7355] mt-1">Must be at least 8 characters long</p>
          </div>
          
          <div className="mb-6">
            <label htmlFor="confirmPassword" className="block text-[#4a3428] text-sm font-bold mb-2">
              Confirm Password
            </label>
            <input
              type="password"
              id="confirmPassword"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleChange}
              className="shadow-sm appearance-none border border-[#e8e0db] rounded-md w-full py-2 px-3 text-[#4a3428] leading-tight focus:outline-none focus:ring-2 focus:ring-[#6f4e37] focus:border-transparent transition-colors duration-200"
              required
            />
          </div>
          
          <div className="flex items-center justify-between">
            <button
              type="submit"
              className="bg-[#4a9b79] hover:bg-[#3b8a6a] text-[#4a3428] font-medium py-2 px-4 rounded-full focus:outline-none focus:shadow-outline w-full transition-colors duration-200 shadow-sm"
              disabled={isLoading}
            >
              {isLoading ? 'Creating Account...' : 'Register'}
            </button>
          </div>
        </form>
        
        <div className="mt-6 text-center">
          <p className="text-[#8b7355]">
            Already have an account?{' '}
            <Link href="/auth/login" className="text-[#6f4e37] hover:text-[#5d4130] font-medium transition-colors duration-200">
              Login
            </Link>
          </p>
        </div>
      </div>
      </div>
      <Footer />
    </div>
  );
}
