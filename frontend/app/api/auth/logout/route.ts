import { NextResponse } from "next/server";
import { cookies } from 'next/headers';

export async function POST(req: Request) {
  try {
    // Forward the logout request to the backend API
    const backendResponse = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/auth/logout`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${cookies().get('auth-token')?.value}`
      },
    });

    // Clear the auth token from cookies regardless of backend response
    cookies().delete('auth-token');
    cookies().delete('user-data');

    const data = await backendResponse.json();

    return NextResponse.json(data, { status: backendResponse.status });
  } catch (error: any) {
    return NextResponse.json(
      { error: error.message || 'Internal server error' },
      { status: 500 }
    );
  }
}