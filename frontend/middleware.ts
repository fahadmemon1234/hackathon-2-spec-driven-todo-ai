import { NextRequest, NextResponse } from 'next/server';
import { auth } from '@/lib/auth';

export function middleware(request: NextRequest) {
  // Define protected routes
  const protectedPaths = ['/tasks'];
  const isProtectedPath = protectedPaths.some(path => 
    request.nextUrl.pathname.startsWith(path)
  );

  // If accessing a protected route without authentication, redirect to login
  if (isProtectedPath) {
    // In a real implementation, we would check the auth session
    // For now, we'll simulate the behavior
    const isAuthenticated = true; // This would come from actual auth check
    
    if (!isAuthenticated) {
      return NextResponse.redirect(new URL('/login', request.url));
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/tasks/:path*', '/profile/:path*'], // Apply middleware to protected routes
};