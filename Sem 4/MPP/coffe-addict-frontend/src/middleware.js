import { NextResponse } from 'next/server';
import { jwtDecode } from 'jwt-decode';

export function middleware(request) {
  // Get the pathname of the request
  const path = request.nextUrl.pathname;

  // Define paths that are considered public (don't need authentication)
  const isPublicPath = 
    path === '/' || 
    path.startsWith('/auth/login') || 
    path.startsWith('/auth/register') ||
    path.startsWith('/auth/verify-2fa');

  // Get the token from the Authorization header or cookies as fallback
  const authHeader = request.headers.get('Authorization');
  const token = authHeader ? 
                authHeader.replace('Bearer ', '') : 
                request.cookies.get('accessToken')?.value || '';

  // Check if token is valid and not expired
  const isValidToken = token ? isTokenValid(token) : false;

  // If the path is not public and there's no valid token, redirect to login
  if (!isPublicPath && !isValidToken) {
    return NextResponse.redirect(new URL('/auth/login', request.nextUrl));
  }

  // If the path is login/register and there's a valid token, redirect to home
  if (isPublicPath && isValidToken && (path.startsWith('/auth/login') || path.startsWith('/auth/register'))) {
    return NextResponse.redirect(new URL('/', request.nextUrl));
  }

  return NextResponse.next();
}

// Helper function to check if a token is valid and not expired
function isTokenValid(token) {
  try {
    const decoded = jwtDecode(token);
    const currentTime = Date.now() / 1000;
    
    // Check if token is expired
    return decoded.exp > currentTime;
  } catch (error) {
    return false;
  }
}

// Configure the middleware to run only for certain paths
export const config = {
  matcher: [
    '/((?!api|_next/static|_next/image|favicon.ico|.*\\.png$).*)',
  ],
};
