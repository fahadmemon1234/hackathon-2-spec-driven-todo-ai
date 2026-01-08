# Feature Specification: Todo AI Chatbot Frontend

**Feature Branch**: `15-todo-ai-chatbot`
**Created**: 2026-01-07
**Status**: Draft
**Input**: User description: "# Frontend Specification - Todo AI Chatbot (Phase III: Basic Level) Project: Todo AI Chatbot Phase: III - Basic Level Functionality Component: Frontend Date: January 07, 2026 ## Overview This specification defines the complete frontend implementation for the Todo AI Chatbot. The frontend provides a conversational interface using OpenAI ChatKit, allowing users to manage todo tasks via natural language. It integrates with the existing FastAPI backend (already implemented) and uses Better Auth for authentication. The frontend must be a Next.js application deployed on Vercel (or similar) and configured with OpenAI's domain allowlist for hosted ChatKit. ## Technology Stack - Framework: Next.js (App Router, TypeScript) - Chat UI: OpenAI ChatKit (@openai/chatkit-js or official package) - Authentication: Better Auth (better-auth) - HTTP Client: Native fetch (or axios if needed) - Styling: Tailwind CSS (recommended) or CSS Modules - State Persistence: localStorage (for conversation_id) - Environment Variables: - NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your-domain-key-from-openai ## Project Structure (/frontend) frontend/ ├── app/ │ ├── api/ │ │ └── auth/[...better-auth]/route.ts # Better Auth handlers │ ├── page.tsx # Main chat page (protected) │ ├── login/page.tsx # Login page (optional if Better Auth provides) │ ├── layout.tsx # Root layout │ └── globals.css ├── components/ │ ├── ChatInterface.tsx # Main ChatKit wrapper component │ ├── Header.tsx # App header with logout │ └── LoadingSpinner.tsx # Optional UI feedback ├── lib/ │ ├── auth.ts # Auth helpers (get session, user_id) │ └── api.ts # API calls to backend ├── public/ │ └── favicon.ico ├── .env.local ├── next.config.js ├── tsconfig.json ├── package.json ├── tailwind.config.js (if using Tailwind) └── README.md ## Functional Requirements ### 1. Authentication - Integrate Better Auth for user sign-up / sign-in (email/password + optional OAuth). - Protect the main chat route (/): redirect unauthenticated users to login. - After successful login, retrieve user_id from session. - Include auth cookies/tokens in requests to backend automatically (Better Auth handles this). - Provide logout functionality. ### 2. Conversation Management - Single conversation per user (no multi-conversation support for basic level). - Store conversation_id in localStorage. - On app load: - Read conversation_id from localStorage. - If exists, send it in API requests to resume context. - If not, omit it — backend will create a new conversation. - After each successful response, update localStorage with the latest conversation_id. ### 3. Chat Interface - Use OpenAI ChatKit component to render the chat UI. - Override default message sending to use custom backend endpoint. - Custom sendMessage handler: - Get current user_id from auth session. - Get conversation_id from localStorage (if any). - POST to: /api/${user_id}/chat - Body: { conversation_id (optional), message } - On success: - Update localStorage.conversation_id with response.conversation_id - Return formatted message for ChatKit: { content: response.response } - On error: Show user-friendly toast/message. - Display assistant responses exactly as returned (with confirmations like "Task added: Buy groceries"). ### 4. API Integration Endpoint: POST /api/{user_id}/chat Request: { "conversation_id": number | undefined, "message": string } Response: { "conversation_id": number, "response": string, "tool_calls"?: array // optional, can log but not required in UI } ### 5. UI/UX Requirements - Clean, minimal design. - Header: "Todo AI Chatbot" + user avatar/email + Logout button. - Chat window: Scrollable message history. - Input box at bottom with send button. - Loading indicator during API calls. - Responsive: Works on mobile and desktop. - Welcome message on first load: "Hi! I can help you manage your todos. Try saying 'Add a task to call mom'." ### 6. OpenAI ChatKit Configuration - Must use hosted ChatKit (requires domain allowlist). - Deployment steps: 1. Deploy frontend to Vercel → get URL (e.g., https://todo-chatbot.vercel.app) 2. Add domain to OpenAI allowlist: https://platform.openai.com/settings/organization/security/domain-allowlist 3. Get domain key → set as NEXT_PUBLIC_OPENAI_DOMAIN_KEY - In code: Pass domainKey prop to ChatKit component. ### 7. Error Handling - Network errors: "Failed to connect. Please try again." - Backend errors (e.g., task not found): Display assistant's graceful response. - Auth errors: Redirect to login. ### 8. Optional Enhancements (Allowed in Basic) - Button to "Start new conversation" (clears localStorage conversation_id). - Auto-focus on input field. - Markdown rendering in assistant responses (if supported by ChatKit). ## Deliverables - Fully working /frontend directory in GitHub repo. - Successful deployment on Vercel with working domain allowlist. - Chatbot that: - Requires login - Sends natural language commands - Receives intelligent responses with task confirmations - Persists conversation across page refreshes - Works after server restarts (stateless backend + DB persistence) ## Notes for Implementation (Agentic Dev Workflow) - Use this spec.txt as input to Claude Code. - Follow: Write spec → Plan → Tasks → Implement (no manual coding). - Test thoroughly: add/list/complete/update/delete tasks via natural language. End of Specification"
**Constitution Compliance**: All features must adhere to project constitution principles

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Authenticate and Access Chat Interface (Priority: P1)

A user wants to securely access the Todo AI Chatbot to manage their tasks through natural language commands. The user visits the application, signs up or logs in using Better Auth, and gains access to the chat interface.

**Why this priority**: Authentication is foundational - without it, users cannot access the core functionality of managing their tasks.

**Independent Test**: Can be fully tested by completing the sign-up/login flow and verifying access to the protected chat page, delivering secure user isolation.

**Acceptance Scenarios**:

1. **Given** an unauthenticated user visiting the app, **When** they try to access the main chat page, **Then** they are redirected to the login page
2. **Given** an unauthenticated user on the login page, **When** they successfully sign up or log in, **Then** they are redirected to the main chat page
3. **Given** an authenticated user, **When** they click logout, **Then** they are logged out and redirected to the login page

---

### User Story 2 - Interact with AI Chatbot to Manage Tasks (Priority: P1)

A user wants to manage their todo tasks using natural language commands through the AI chatbot interface. They can add, list, complete, update, and delete tasks by chatting with the bot.

**Why this priority**: This is the core functionality of the application - enabling natural language task management.

**Independent Test**: Can be fully tested by sending various natural language commands to the chatbot and verifying the backend processes them correctly, delivering the primary value proposition.

**Acceptance Scenarios**:

1. **Given** an authenticated user in the chat interface, **When** they send a message like "Add a task to buy groceries", **Then** the chatbot responds with confirmation and the task appears in their task list
2. **Given** a user with existing tasks, **When** they ask "Show my tasks", **Then** the chatbot lists their tasks
3. **Given** a user with tasks, **When** they say "Complete task 1", **Then** the chatbot confirms the task is completed

---

### User Story 3 - Maintain Conversation Context Across Sessions (Priority: P2)

A user wants their conversation with the AI chatbot to maintain context even after refreshing the page or returning later, so they can continue their task management seamlessly.

**Why this priority**: Improves user experience by maintaining continuity in their interaction with the AI.

**Independent Test**: Can be fully tested by starting a conversation, refreshing the page, and continuing the conversation with context-aware responses, delivering improved UX.

**Acceptance Scenarios**:

1. **Given** a user engaged in a conversation, **When** they refresh the page, **Then** their conversation context is preserved
2. **Given** a user who left a conversation and returns later, **When** they start chatting again, **Then** the AI can reference earlier parts of the conversation

---

### User Story 4 - Receive Responsive and Accessible UI Experience (Priority: P2)

A user wants to access the Todo AI Chatbot from different devices and screen sizes with a consistent, responsive interface that provides feedback during operations.

**Why this priority**: Ensures the application is usable across different contexts and devices, expanding accessibility.

**Independent Test**: Can be fully tested by using the interface on different screen sizes and verifying responsive design and loading states, delivering consistent UX.

**Acceptance Scenarios**:

1. **Given** a user on a mobile device, **When** they interact with the chat interface, **Then** the UI adapts appropriately to the smaller screen
2. **Given** a user sending a message to the chatbot, **When** the request is processing, **Then** they see a loading indicator
3. **Given** a user on the main chat page, **When** they first load the page, **Then** they see a welcome message with usage instructions

---

### Edge Cases

- What happens when the user's authentication token expires during a session?
- How does the system handle network connectivity issues during chat interactions?
- What occurs when the OpenAI ChatKit service is temporarily unavailable?
- How does the system behave when localStorage is disabled or full?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST authenticate users via Better Auth (email/password + optional OAuth)
- **FR-002**: System MUST protect the main chat route and redirect unauthenticated users to login
- **FR-003**: System MUST integrate with OpenAI ChatKit for the conversational interface
- **FR-004**: System MUST store conversation_id in localStorage to maintain context across sessions
- **FR-005**: System MUST override ChatKit's default message sending to use the custom backend endpoint
- **FR-006**: System MUST send authenticated requests to the backend API with user_id and conversation_id
- **FR-007**: System MUST update localStorage with the latest conversation_id after successful responses
- **FR-008**: System MUST display assistant responses exactly as returned from the backend
- **FR-009**: System MUST provide a clean, responsive UI that works on mobile and desktop
- **FR-010**: System MUST show loading indicators during API calls
- **FR-011**: System MUST display a welcome message on first load with usage instructions
- **FR-012**: System MUST handle network errors gracefully with user-friendly messages
- **FR-013**: System MUST redirect to login when authentication errors occur
- **FR-014**: System MUST provide logout functionality that clears user session

### Key Entities *(include if feature involves data)*

- **User**: Represents an authenticated user with session management via Better Auth
- **Conversation**: Represents a chat session with an ID stored in localStorage to maintain context
- **Message**: Represents an exchange between user and AI assistant, containing text content and metadata

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can complete the sign-up/login process and access the chat interface within 2 minutes
- **SC-002**: Natural language commands for task management (add, list, complete, update, delete) are processed with at least 90% accuracy
- **SC-003**: The application maintains conversation context across page refreshes and browser sessions
- **SC-004**: The UI is responsive and usable on screen sizes ranging from 320px (mobile) to 1920px (desktop)
- **SC-005**: 95% of users can successfully complete their first task management action (e.g., adding a task) without assistance
- **SC-006**: The application loads and becomes interactive within 3 seconds on a standard broadband connection
- **SC-007**: The application handles network errors gracefully with appropriate user feedback 100% of the time