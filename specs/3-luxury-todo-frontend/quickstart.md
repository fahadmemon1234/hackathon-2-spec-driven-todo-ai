# Quickstart Guide: Luxury Todo Frontend

## Prerequisites
- Node.js 18+ installed
- npm or yarn package manager
- Better Auth compatible environment

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd todo-app-frontend
   ```

2. **Install dependencies**
   ```bash
   cd frontend
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

## API Integration
- The frontend connects to the backend API at `http://localhost:8000`
- All API requests automatically include the JWT token from Better Auth session
- Mock API responses are used during development until backend is available

## Key Features
- User authentication (signup/login)
- Create, read, update, delete tasks
- Mark tasks as complete/incomplete
- Luxury dark-themed UI with specified color palette
- Responsive design for mobile and desktop
- Loading states and empty states
- Toast notifications for user feedback