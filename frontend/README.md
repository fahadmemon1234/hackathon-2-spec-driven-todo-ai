# Luxury Todo Frontend

A premium todo application with luxury design and authentication features.

## Features

- User authentication (signup/login)
- Create, read, update, delete tasks
- Mark tasks as complete/incomplete
- Luxury dark-themed UI with specified color palette
- Responsive design for mobile and desktop
- Loading states and empty states
- Toast notifications for user feedback

## Setup Instructions

1. **Navigate to the frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   Create a `.env.local` file in the frontend directory:
   ```env
   BETTER_AUTH_SECRET=your-super-secret-jwt-secret-here
   BETTER_AUTH_URL=http://localhost:3000
   ```

4. **Run the development server**
   ```bash
   npm run dev
   ```

5. **Access the application**
   Open [http://localhost:3000](http://localhost:3000) in your browser

## Tech Stack

- Next.js 14
- TypeScript
- Tailwind CSS
- Better Auth
- Sonner (for notifications)
- React Hook Form

## Architecture

- App Router structure
- Component-based architecture
- API client with JWT auto-attachment
- Context API for authentication state