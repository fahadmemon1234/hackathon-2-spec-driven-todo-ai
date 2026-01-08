# Data Model - Todo AI Chatbot Frontend

## Entities

### User
Represents an authenticated user with session management via Better Auth

**Fields:**
- id: string (unique identifier from Better Auth)
- email: string (user's email address)
- name: string (optional, user's name)

**Relationships:**
- Has many Conversations (one-to-many)

### Conversation
Represents a chat session with an ID stored in localStorage to maintain context

**Fields:**
- id: number (unique identifier from backend)
- userId: string (foreign key to User)
- createdAt: Date (timestamp when conversation started)
- updatedAt: Date (timestamp of last activity)

**Relationships:**
- Belongs to User (many-to-one)
- Has many Messages (one-to-many)

### Message
Represents an exchange between user and AI assistant, containing text content and metadata

**Fields:**
- id: string (unique identifier)
- conversationId: number (foreign key to Conversation)
- role: 'user' | 'assistant' (sender of the message)
- content: string (the actual message text)
- timestamp: Date (when the message was sent/received)

**Relationships:**
- Belongs to Conversation (many-to-one)

## State Transitions

### User Session States
- Unauthenticated → Authenticating → Authenticated
- Authenticated → Logging Out → Unauthenticated
- Authenticated → Session Expired → Unauthenticated

### Conversation States
- New (no conversation_id in localStorage)
- Active (has conversation_id, ongoing interaction)
- Paused (user navigated away but conversation_id exists)
- Resumed (returning to existing conversation)

## Validation Rules

### User Validation
- Email must be in valid email format
- User must be authenticated to access chat functionality

### Conversation Validation
- conversation_id must be a positive integer when present
- conversation_id must exist in backend when resuming

### Message Validation
- Content must not be empty
- Role must be either 'user' or 'assistant'
- Timestamp must be a valid date

## Data Flow

1. User authenticates → Session established
2. App checks localStorage for conversation_id
3. If exists → Resume conversation with backend
4. If not exists → Start new conversation with backend
5. User sends message → Store in UI, send to backend
6. Backend responds → Update UI, store conversation_id in localStorage
7. Repeat for each message exchange
8. On logout → Clear sensitive data from localStorage