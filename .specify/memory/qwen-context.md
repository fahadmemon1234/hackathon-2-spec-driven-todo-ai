# Qwen Context - Todo AI Chatbot Frontend

## Project Context
- Project: Todo AI Chatbot (Phase III: Basic Level)
- Component: Frontend
- Framework: Next.js (App Router, TypeScript)
- UI Library: Tailwind CSS
- Authentication: Better Auth
- Chat Interface: Custom implementation (no official OpenAI ChatKit)
- Backend Integration: FastAPI backend with AI processing
- Deployment: Vercel

## Key Technologies
- Next.js 14+ with App Router
- React 18+
- TypeScript
- Tailwind CSS
- Better Auth for authentication
- OpenAI API (via custom integration)
- Node.js 18+

## Architecture Notes
- The frontend uses a custom chat interface rather than an official OpenAI ChatKit library
- Authentication is handled via Better Auth with session management
- Conversation state is maintained using localStorage
- API communication follows the contract: POST /api/{user_id}/chat
- Request format: { conversation_id (optional), message }
- Response format: { conversation_id, response, tool_calls (optional) }

## Important Implementation Details
- Use Next.js App Router for page structure
- Implement protected routes using Better Auth session management
- Create a custom chat UI component that integrates with the backend AI service
- Handle conversation persistence using localStorage
- Implement proper error handling for network requests and authentication
- Ensure responsive design for mobile and desktop

## File Structure
- App Router pages in /app directory
- Components in /components directory
- Utility functions in /lib directory
- API routes for auth in /app/api/auth/[...better-auth]/route.ts
- Environment variables using Next.js standard approach

## Environment Variables
- NEXT_PUBLIC_BETTER_AUTH_URL
- BETTER_AUTH_SECRET
- NEXT_PUBLIC_API_BASE_URL
- NEXT_PUBLIC_OPENAI_DOMAIN_KEY (if needed)

## API Contract
- Authentication: Better Auth endpoints
- Chat API: POST /api/{user_id}/chat
- Request: { conversation_id (optional), message }
- Response: { conversation_id, response, tool_calls (optional) }

## Common Patterns
- Use server components for auth session checks
- Use client components for interactive UI elements
- Implement proper TypeScript typing throughout
- Follow Next.js best practices for data fetching
- Use Tailwind CSS for styling with responsive design