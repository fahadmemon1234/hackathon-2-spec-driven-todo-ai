import { NextResponse } from "next/server";
import { cookies } from 'next/headers';

export async function GET(req: Request) {
  try {
    const token = cookies().get('auth-token')?.value;

    if (!token) {
      return NextResponse.json({ user: null }, { status: 200 });
    }

    // Forward the request to the backend API to validate the token
    // Use BACKEND_INTERNAL_URL for server-side calls, fallback to NEXT_PUBLIC_BACKEND_URL
    const backendUrl = process.env.BACKEND_INTERNAL_URL || process.env.NEXT_PUBLIC_BACKEND_URL;
    const backendResponse = await fetch(`${backendUrl}/api/auth/session`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
    });

    if (backendResponse.ok) {
      const data = await backendResponse.json();
      return NextResponse.json(data, { status: 200 });
    } else {
      // If the token is invalid, return no user
      return NextResponse.json({ user: null }, { status: 200 });
    }
  } catch (error: any) {
    return NextResponse.json(
      { error: error.message || 'Internal server error' },
      { status: 500 }
    );
  }
}