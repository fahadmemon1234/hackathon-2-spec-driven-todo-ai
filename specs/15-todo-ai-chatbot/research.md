# Research Findings - Todo AI Chatbot Frontend

## 1. OpenAI ChatKit Package Information

### Decision: Use @openai/openai package for API calls, but implement chat UI separately
**Note**: After research, it appears OpenAI doesn't have an official "ChatKit" UI library as described in the spec. Instead, we'll implement a custom chat UI that communicates with the OpenAI API directly or with our backend that handles the AI processing.

### Rationale:
- OpenAI's official packages are primarily for API access (@openai/openai)
- There is no official "ChatKit" UI library from OpenAI
- The spec likely refers to a generic chat UI component that connects to OpenAI services
- We'll create a custom chat interface that integrates with our backend's AI functionality

### Alternatives Considered:
- Using third-party chat UI libraries like react-chat-elements or similar
- Creating a completely custom chat interface from scratch
- Using a commercial chat UI solution

## 2. Better Auth Integration with Next.js App Router

### Decision: Use Better Auth with Next.js App Router following official documentation
- Install `better-auth` and `@better-auth/react`
- Configure the auth client and server actions
- Use the `useSession` hook for client-side session management
- Use server actions or middleware for protected routes

### Rationale:
- Better Auth officially supports Next.js App Router
- Provides both client and server-side session management
- Offers email/password and social login options
- Integrates well with React applications

### Implementation Pattern:
```typescript
// lib/auth.ts
import { betterAuth } from "better-auth";
import { nextjs } from "@better-auth/nextjs";

export const auth = betterAuth({
  // configuration options
});

export const { getServerSession } = nextjs(auth, {
  basePath: "/api/auth",
});
```

## 3. Backend API Endpoint Details

### Decision: Follow the API specification provided in the feature spec
- Endpoint: POST /api/{user_id}/chat
- Request: { conversation_id (optional), message }
- Response: { conversation_id, response, tool_calls (optional) }

### Rationale:
- This matches the existing backend implementation
- Maintains consistency with the established API contract
- Supports conversation context management

### Error Handling:
- Network errors: Catch fetch errors and display user-friendly messages
- Backend errors: Display error messages from the API response
- Authentication errors: Redirect to login page

## 4. Custom Chat UI Implementation

### Decision: Create a custom chat interface using React and Tailwind CSS
- Implement message history display
- Create input area with send button
- Add loading indicators during API calls
- Handle scroll behavior for new messages

### Rationale:
- No official OpenAI ChatKit UI library exists
- Custom implementation allows for complete control over UI/UX
- Can be tailored specifically to the todo management use case
- Maintains consistency with the application's design

## 5. TypeScript Types for Application

### Decision: Define specific TypeScript interfaces for all major data structures

```typescript
// types/index.ts
export interface User {
  id: string;
  email: string;
  name?: string;
}

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export interface Conversation {
  id: number;
  userId: string;
  messages: Message[];
  createdAt: Date;
  updatedAt: Date;
}

export interface ChatRequest {
  message: string;
  conversation_id?: number;
}

export interface ChatResponse {
  conversation_id: number;
  response: string;
  tool_calls?: any[]; // Optional, as per spec
}
```

### Rationale:
- Strong typing improves code quality and reduces runtime errors
- Makes the codebase more maintainable
- Enables better IDE support and autocompletion
- Aligns with TypeScript-first approach specified in the feature spec

## 6. Environment Configuration

### Decision: Use standard Next.js environment variable handling
- Create .env.local file for local development
- Use NEXT_PUBLIC_OPENAI_DOMAIN_KEY as specified in the feature spec
- For actual OpenAI API access, use NEXT_PUBLIC_OPENAI_API_KEY if needed

### Rationale:
- Standard Next.js practice
- Secure handling of sensitive information
- Easy configuration for different environments