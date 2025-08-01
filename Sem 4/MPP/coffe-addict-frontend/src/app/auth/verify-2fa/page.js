'use client';

import { useState, useEffect, Suspense } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { useAuth } from '../../utils/AuthContext';
import { Header } from '../../components/homeWindow/Header';
import { Footer } from '../../components/Footer';

function Verify2FAContent() {
  const [code, setCode] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [formError, setFormError] = useState('');
  const [jobId, setJobId] = useState('');
  const [phoneHint, setPhoneHint] = useState('');
  const [message, setMessage] = useState('');
  const [timeLeft, setTimeLeft] = useState(300); // 5 minutes in seconds
  const { verify2FA, error, isAuthenticated } = useAuth();
  const router = useRouter();
  const searchParams = useSearchParams();

  useEffect(() => {
    // Get 2FA data from URL params
    const jobIdParam = searchParams.get('jobId');
    const phoneHintParam = searchParams.get('phoneHint');
    const messageParam = searchParams.get('message');

    if (!jobIdParam) {
      // If no job ID, redirect to login
      router.push('/auth/login');
      return;
    }

    setJobId(jobIdParam);
    setPhoneHint(phoneHintParam || '***-***-****');
    setMessage(messageParam || 'A verification code has been sent to your phone');
  }, [searchParams, router]);

  // Redirect if already authenticated
  useEffect(() => {
    if (isAuthenticated) {
      router.push('/');
    }
  }, [isAuthenticated, router]);

  // Countdown timer effect
  useEffect(() => {
    if (timeLeft > 0) {
      const timer = setTimeout(() => setTimeLeft(timeLeft - 1), 1000);
      return () => clearTimeout(timer);
    } else if (timeLeft === 0) {
      setFormError('Verification code has expired. Please try logging in again.');
    }
  }, [timeLeft]);

  const handleChange = (e) => {
    let value = e.target.value.replace(/\D/g, ''); // Only allow digits
    if (value.length <= 6) {
      setCode(value);
      setFormError('');
      
      // Auto-submit when 6 digits are entered
      if (value.length === 6 && !isLoading) {
        setTimeout(() => {
          handleSubmit({ preventDefault: () => {} });
        }, 300);
      }
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (code.length !== 6) {
      setFormError('Please enter a 6-digit verification code');
      return;
    }
    
    if (!jobId) {
      setFormError('Invalid verification session. Please try logging in again.');
      return;
    }
    
    setIsLoading(true);
    
    try {
      const result = await verify2FA(jobId, code);
      if (result.success) {
        router.push('/');
      } else {
        setFormError(result.error || 'Verification failed');
      }
    } catch (err) {
      console.error('2FA verification error:', err);
      setFormError('Verification failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleResendCode = () => {
    // For now, redirect back to login to resend
    router.push('/auth/login');
  };

  // Format time as MM:SS
  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="min-h-screen flex flex-col bg-[#fdf8f5]">
      <Header />
      <div className="flex-grow flex items-center justify-center pb-20">
        <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md border border-[#e8e0db] mx-4">
          <div className="text-center mb-6">
            <h1 className="text-2xl font-bold mb-2 text-[#4a3428]">Two-Factor Authentication</h1>
            <p className="text-[#8b7355] text-sm mb-2">{message}</p>
            <p className="text-[#8b7355] text-sm">Sent to: {phoneHint}</p>
          </div>
          
          {(error || formError) && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4" role="alert">
              <span className="block sm:inline">{formError || error}</span>
            </div>
          )}
        
          <form onSubmit={handleSubmit}>
            <div className="mb-6">
              <label htmlFor="code" className="block text-[#4a3428] text-sm font-bold mb-4 text-center">
                Verification Code
              </label>
              
              {/* Individual digit input boxes for better UX */}
              <div className="flex justify-center gap-2 mb-3">
                {[0, 1, 2, 3, 4, 5].map((index) => (
                  <input
                    key={index}
                    type="text"
                    value={code[index] || ''}
                    onChange={(e) => {
                      const value = e.target.value.replace(/\D/g, '');
                      if (value.length <= 1) {
                        const newCode = code.split('');
                        newCode[index] = value;
                        const updatedCode = newCode.join('').slice(0, 6);
                        setCode(updatedCode);
                        setFormError('');
                        
                        // Auto-focus next input
                        if (value && index < 5) {
                          const nextInput = e.target.parentElement.children[index + 1];
                          if (nextInput) nextInput.focus();
                        }
                        
                        // Auto-submit when 6 digits are entered
                        if (updatedCode.length === 6 && !isLoading) {
                          setTimeout(() => {
                            handleSubmit({ preventDefault: () => {} });
                          }, 300);
                        }
                      }
                    }}
                    onKeyDown={(e) => {
                      // Handle backspace
                      if (e.key === 'Backspace' && !code[index] && index > 0) {
                        const prevInput = e.target.parentElement.children[index - 1];
                        if (prevInput) {
                          prevInput.focus();
                          const newCode = code.split('');
                          newCode[index - 1] = '';
                          setCode(newCode.join(''));
                        }
                      }
                    }}
                    onPaste={(e) => {
                      e.preventDefault();
                      const pasteData = e.clipboardData.getData('text').replace(/\D/g, '').slice(0, 6);
                      setCode(pasteData);
                      if (pasteData.length === 6 && !isLoading) {
                        setTimeout(() => {
                          handleSubmit({ preventDefault: () => {} });
                        }, 300);
                      }
                    }}
                    className="w-12 h-12 text-center text-lg font-mono border border-[#e8e0db] rounded-md focus:outline-none focus:ring-2 focus:ring-[#6f4e37] focus:border-transparent transition-colors duration-200"
                    maxLength="1"
                    autoFocus={index === 0}
                  />
                ))}
              </div>
              
              {/* Hidden input for form submission */}
              <input
                type="hidden"
                id="code"
                name="code"
                value={code}
              />
              
              <p className="text-[#8b7355] text-xs text-center">Enter the 6-digit code sent to your phone</p>
            </div>
            
            <div className="flex flex-col gap-3">
              <button
                type="submit"
                className="bg-[#6f4e37] hover:bg-[#5d4130] text-white font-medium py-3 px-4 rounded-full focus:outline-none focus:shadow-outline w-full transition-colors duration-200 shadow-sm disabled:opacity-50"
                disabled={isLoading || code.length !== 6}
              >
                {isLoading ? 'Verifying...' : 'Verify Code'}
              </button>
              
              <button
                type="button"
                onClick={handleResendCode}
                className="bg-transparent hover:bg-[#f5f5f5] text-[#6f4e37] font-medium py-2 px-4 rounded-full border border-[#6f4e37] transition-colors duration-200"
                disabled={isLoading}
              >
                Resend Code
              </button>
            </div>
          </form>
          
          <div className="mt-6 text-center">
            <p className="text-[#8b7355] text-sm">
              Having trouble?{' '}
              <button 
                onClick={() => router.push('/auth/login')}
                className="text-[#6f4e37] hover:text-[#5d4130] font-medium transition-colors duration-200"
              >
                Back to Login
              </button>
            </p>
          </div>

          <div className="mt-4 text-center">
            <p className="text-[#8b7355] text-xs">
              {formError ? formError : `Code expires in: ${formatTime(timeLeft)}`}
            </p>
          </div>
        </div>
      </div>
      <Footer index={4} />
    </div>
  );
}

// Loading component for Suspense fallback
function LoadingFallback() {
  return (
    <div className="min-h-screen flex flex-col bg-[#fdf8f5]">
      <Header />
      <div className="flex-grow flex items-center justify-center pb-20">
        <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md border border-[#e8e0db] mx-4">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-[#6f4e37] mx-auto mb-4"></div>
            <p className="text-[#4a3428]">Loading...</p>
          </div>
        </div>
      </div>
      <Footer index={4} />
    </div>
  );
}

export default function Verify2FA() {
  return (
    <Suspense fallback={<LoadingFallback />}>
      <Verify2FAContent />
    </Suspense>
  );
}
