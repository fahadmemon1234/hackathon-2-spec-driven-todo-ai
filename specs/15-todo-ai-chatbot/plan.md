# Implementation Plan - Todo AI Chatbot Frontend (Phase III: Basic Level)

Project: Todo AI Chatbot
Component: Frontend (Next.js + OpenAI ChatKit + Better Auth)
Goal: Build a fully working frontend that integrates with the existing backend, supports authentication, and provides a natural language chat interface for todo management.
Approach: Strictly follow Agentic Dev Stack workflow → Use this plan with Claude Code/Spec-Kit Plus. NO manual coding.

## Overall Strategy
1. Use this plan.txt as input to Claude Code.
2. Break the plan into small, sequential tasks (5-10 tasks total).
3. Implement one task at a time via Claude → Review output → Commit → Next task.
4. Final step: Full end-to-end test and deployment preparation.

## Phase 1: Project Setup & Boilerplate (Tasks 1-3)

Task 1: Initialize Next.js Project
- Create a new Next.js app (App Router, TypeScript) in /frontend folder.
- Add Tailwind CSS (recommended for styling).
- Add necessary dependencies:
  - better-auth
  - @better-auth/react (if available)
  - @openai/chatkit-js (or correct official ChatKit package name)
  - typescript, @types/node, @types/react, etc.
- Set up basic folder structure as per spec:
  app/, components/, lib/, public/
- Create .env.local with placeholder NEXT_PUBLIC_OPENAI_DOMAIN_KEY=placeholder
- Add basic README.md with setup instructions.

Task 2: Configure Better Auth (Authentication)
- Set up Better Auth in the project.
- Create API route: app/api/auth/[...better-auth]/route.ts
- Configure Better Auth with at least email/password sign-in (add Google OAuth if easy).
- Create simple login page (app/login/page.tsx) with sign-in form.
- Create auth utility in lib/auth.ts to get session and user_id on server/client.
- Add basic protected route logic: redirect to /login if not authenticated.

Task 3: Create Root Layout and Header
- Update app/layout.tsx with basic HTML structure and Tailwind.
- Create components/Header.tsx with:
  - App title "Todo AI Chatbot"
  - Display user email/name
  - Logout button
- Include Header in root layout.
- Add global styles (globals.css + Tailwind).

## Phase 2: Core Chat Functionality (Tasks 4-7)

Task 4: Create ChatInterface Component (Skeleton)
- Create components/ChatInterface.tsx
- Add placeholder UI: welcome message, message list (empty), input box.
- Temporary static messages to verify layout (e.g., "Hi! I can help you manage your todos.").

Task 5: Integrate OpenAI ChatKit
- Install and import the official OpenAI ChatKit component.
- Replace placeholder with real <ChatKit /> component in ChatInterface.tsx.
- Pass domainKey={process.env.NEXT_PUBLIC_OPENAI_DOMAIN_KEY}
- Configure basic props (theme, placeholder text, etc.).
- Test that ChatKit renders correctly locally (localhost should work without domain key).

Task 6: Custom Message Sending to Backend
- Create lib/api.ts with a function sendMessageToBackend({ message, conversationId, userId })
  - Use fetch to POST /api/${userId}/chat
  - Include credentials/cookies for auth.
  - Handle JSON response and errors.
- Override ChatKit's message sending:
  - Use onSend prop or custom send handler as per ChatKit docs.
  - Get userId from auth session.
  - Get conversationId from localStorage.getItem('conversation_id')
  - Call sendMessageToBackend
  - On success:
    - localStorage.setItem('conversation_id', data.conversation_id)
    - Return formatted message { role: 'assistant', content: data.response } for ChatKit
  - Show loading state during request.

Task 7: Conversation Persistence & Resume
- On component mount (in ChatInterface or page.tsx):
  - If localStorage has conversation_id, keep it for resumption.
  - No need to pre-load history (backend handles it via conversation_id).
- Add optional "Start new conversation" button that clears localStorage.conversation_id and reloads.

## Phase 3: Polish, Error Handling & Deployment Prep (Tasks 8-10)

Task 8: UI Polish & UX Improvements
- Add loading indicator during message send.
- Auto-scroll to bottom on new messages.
- Responsive design fixes (mobile-friendly).
- Welcome message on first load (if no history).
- Friendly error toasts/messages on failures.

Task 9: Full Integration Testing (Manual Review Step)
- Test end-to-end flows:
  - Sign up / login
  - Send "Add a task to buy milk" → confirm task added
  - "Show my tasks" → see list
  - "Mark task 1 as complete"
  - "Delete task 1"
  - Page refresh → conversation resumes
  - Logout/login → new conversation starts (or resumes if user_id same)

Task 10: Deployment Preparation
- Update README.md with:
  - Setup instructions (npm install, .env.local)
  - How to get and set NEXT_PUBLIC_OPENAI_DOMAIN_KEY
  - Vercel deployment steps
  - Note about OpenAI domain allowlist requirement
- Add vercel.json if needed for routing.
- Ensure build succeeds: npm run build

## Completion Criteria
- Frontend runs locally and connects to backend.
- Authentication works.
- Natural language todo management works fully.
- Conversation persists across refreshes.
- Ready for Vercel deployment (domain allowlist step pending).

Total Tasks: 10
Estimated Claude Code Iterations: 10-15 (one per task + minor fixes)

Next Step: Feed this plan.txt to Claude Code and start with Task 1.

End of Plan

## Technical Context

### Known Elements
- **Frontend Framework**: Next.js with App Router and TypeScript
- **Chat UI**: OpenAI ChatKit
- **Authentication**: Better Auth
- **Styling**: Tailwind CSS
- **State Persistence**: localStorage for conversation_id
- **Backend Integration**: Existing FastAPI backend with /api/{user_id}/chat endpoint
- **Environment Variables**: NEXT_PUBLIC_OPENAI_DOMAIN_KEY for ChatKit domain allowlist
- **Deployment**: Vercel
- **Project Structure**: As specified in feature spec

### Unknown Elements
- **OpenAI ChatKit Package Name**: NEEDS CLARIFICATION - Exact package name and version to use
- **Better Auth Integration Details**: NEEDS CLARIFICATION - Specific configuration options and best practices for Next.js App Router
- **Backend API Endpoint Details**: NEEDS CLARIFICATION - Exact request/response format and error handling
- **OpenAI ChatKit Customization**: NEEDS CLARIFICATION - How to properly override the message sending functionality
- **TypeScript Types**: NEEDS CLARIFICATION - Specific types needed for messages, conversations, and API responses

## Constitution Check

### Compliance Verification
- **AI-Centric Development**: All code will be generated via AI tools (Claude Code primarily, with Qwen for planning)
- **Spec-Driven Approach**: Following the formal specification created in spec.md
- **Clean Code and Modularity**: Will adhere to Next.js best practices and modular design
- **Transparency and Iteration**: All development will be documented in appropriate files
- **Scalability Focus**: Designing with future phases in mind
- **Ethical AI Use**: Ensuring secure and efficient code generation

### Technology Stack Compliance
- **Frontend Framework**: Next.js (approved for frontend development)
- **Authentication**: Better Auth (compliant with spec)
- **Styling**: Tailwind CSS (compliant with spec)
- **Environment Management**: Will use standard Next.js practices

## Gates Evaluation

### Gate 1: Architecture Alignment
✅ PASSES - Architecture aligns with feature specification and project constitution

### Gate 2: Technology Stack Compliance
✅ PASSES - All selected technologies comply with project constitution

### Gate 3: Implementation Feasibility
✅ PASSES - Implementation approach is feasible with available tools and technologies

### Gate 4: Security Considerations
✅ PASSES - Using established authentication (Better Auth) and following security best practices

## Phase 0: Research & Unknown Resolution

### Research Tasks
1. Research the correct OpenAI ChatKit package name and integration patterns
2. Research Better Auth best practices for Next.js App Router
3. Research the exact API endpoint format and response structure for the backend
4. Research how to properly customize OpenAI ChatKit's message sending functionality
5. Research necessary TypeScript types for the application

## Phase 1: Design & Contracts

### Data Model
- User: Authentication data from Better Auth
- Conversation: ID stored in localStorage
- Message: Content exchanged between user and AI assistant

### API Contracts
- POST /api/{user_id}/chat: Send message to backend AI service
  - Request: { conversation_id (optional), message }
  - Response: { conversation_id, response, tool_calls (optional) }

### Quickstart Guide
- Setup instructions for local development
- Environment variable configuration
- Running the development server
- Testing the authentication flow