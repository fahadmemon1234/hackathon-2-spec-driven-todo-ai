# Quickstart Guide - Todo AI Chatbot Frontend

## Prerequisites

- Node.js 18+ installed
- npm or yarn package manager
- Access to the backend API (FastAPI server running)
- Better Auth secret key
- (Optional) OpenAI API key if using direct OpenAI integration

## Setup Instructions

### 1. Clone and Navigate to Project
```bash
cd F:\Programing\governor Inititative Program IT\Ai\Hackathon 2\todo-app-Phase-3\frontend
```

### 2. Install Dependencies
```bash
npm install
# or
yarn install
```

### 3. Environment Configuration
Create a `.env.local` file in the frontend directory with the following:

```env
# Better Auth Configuration
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-better-auth-secret

# Backend API Configuration
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000

# OpenAI Configuration (if using direct integration)
NEXT_PUBLIC_OPENAI_API_KEY=your-openai-api-key
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your-openai-domain-key
```

### 4. Run Development Server
```bash
npm run dev
# or
yarn dev
```

The application will be available at `http://localhost:3000`

## Key Features and Usage

### Authentication
1. Visit the application at `http://localhost:3000`
2. If not authenticated, you'll be redirected to the login page
3. Sign up with email/password or use OAuth if configured
4. After successful authentication, you'll be redirected to the chat interface

### Using the Chat Interface
1. Once logged in, you'll see the main chat interface
2. Type your natural language commands in the input box:
   - "Add a task to buy groceries"
   - "Show my tasks"
   - "Mark task 1 as complete"
   - "Delete task 2"
3. The AI assistant will respond with confirmations and results

### Conversation Persistence
- Your conversation context is maintained across page refreshes
- The conversation ID is stored in localStorage
- When you return to the app, your conversation will resume

## Project Structure

```
frontend/
├── app/                 # Next.js App Router pages
│   ├── api/             # API routes (Better Auth)
│   ├── login/           # Login page
│   ├── layout.tsx       # Root layout
│   └── page.tsx         # Main chat page
├── components/          # React components
│   ├── ChatInterface.tsx # Main chat UI component
│   ├── Header.tsx       # App header with user info
│   └── ...              # Other UI components
├── lib/                 # Utility functions
│   ├── auth.ts          # Authentication helpers
│   └── api.ts           # API client functions
├── public/              # Static assets
├── .env.local           # Environment variables
├── next.config.js       # Next.js configuration
├── package.json         # Dependencies and scripts
└── tsconfig.json        # TypeScript configuration
```

## Development Commands

```bash
# Run development server
npm run dev

# Build for production
npm run build

# Run production build locally
npm start

# Run linting
npm run lint

# Run tests (if any exist)
npm run test
```

## Troubleshooting

### Common Issues

1. **Authentication not working**
   - Verify `BETTER_AUTH_SECRET` is set correctly
   - Check that the backend auth service is running

2. **Chat not connecting to backend**
   - Verify `NEXT_PUBLIC_API_BASE_URL` points to the running backend
   - Check browser console for network errors

3. **OpenAI ChatKit not loading**
   - Ensure `NEXT_PUBLIC_OPENAI_DOMAIN_KEY` is set if required
   - Note: The implementation uses a custom chat UI rather than an official ChatKit library

### Environment Variables
Make sure all required environment variables are set in `.env.local`:
- `NEXT_PUBLIC_BETTER_AUTH_URL` - URL of your Better Auth service
- `BETTER_AUTH_SECRET` - Secret key for Better Auth
- `NEXT_PUBLIC_API_BASE_URL` - URL of your backend API
- `NEXT_PUBLIC_OPENAI_DOMAIN_KEY` - Domain key for OpenAI services (if applicable)

## Deployment

### To Vercel
1. Push your code to a Git repository
2. Connect your repository to Vercel
3. Add the required environment variables in Vercel dashboard
4. Deploy

### Environment Variables for Production
When deploying, ensure these variables are set in your hosting environment:
- `NEXT_PUBLIC_BETTER_AUTH_URL` - Production URL of your Better Auth service
- `BETTER_AUTH_SECRET` - Secret key for Better Auth (not public)
- `NEXT_PUBLIC_API_BASE_URL` - Production URL of your backend API
- `NEXT_PUBLIC_OPENAI_DOMAIN_KEY` - Domain key for OpenAI services (if applicable)