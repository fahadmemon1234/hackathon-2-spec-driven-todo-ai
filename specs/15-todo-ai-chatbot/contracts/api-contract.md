# API Contracts - Todo AI Chatbot Frontend

## Authentication API

### POST /api/auth/[...better-auth]/route.ts
Better Auth API route handler for authentication operations.

**Request:**
- Method: Various (POST, GET depending on auth action)
- Headers: Content-Type: application/json
- Body: Varies by auth action (sign-in, sign-up, etc.)

**Response:**
- Success: 200 OK with session/token data
- Error: 400/401/500 with error details

## Chat API

### POST /api/{user_id}/chat
Send a message to the AI chatbot and receive a response.

**Request:**
- Method: POST
- Endpoint: `/api/{user_id}/chat`
- Headers: 
  - Content-Type: application/json
  - Authorization: Bearer {token} (if required)
- Body:
```json
{
  "conversation_id": {
    "type": "integer",
    "minimum": 1,
    "description": "Optional. ID of the conversation to continue. If omitted, a new conversation will be started.",
    "example": 123
  },
  "message": {
    "type": "string",
    "minLength": 1,
    "maxLength": 1000,
    "description": "The message content from the user",
    "example": "Add a task to buy groceries"
  }
}
```

**Response:**
- Success (200 OK):
```json
{
  "conversation_id": {
    "type": "integer",
    "minimum": 1,
    "description": "ID of the conversation (new or existing)",
    "example": 123
  },
  "response": {
    "type": "string",
    "description": "The AI's response to the user's message",
    "example": "Task added: Buy groceries"
  },
  "tool_calls": {
    "type": "array",
    "items": {
      "type": "object"
    },
    "description": "Optional. Tool calls made by the AI as part of processing the request",
    "example": [],
    "nullable": true
  }
}
```

- Error (4xx/5xx):
```json
{
  "error": {
    "type": "string",
    "description": "Error message describing what went wrong",
    "example": "Invalid user ID"
  }
}
```

## Protected Route Middleware

### Server-Side Session Check
Middleware to protect routes that require authentication.

**Logic:**
1. Check for valid session/cookie
2. If valid, allow access to route
3. If invalid/expired, redirect to login page

## Frontend API Client Functions

### sendMessageToBackend({ message, conversationId, userId })

**Parameters:**
- message: string - The user's message to send
- conversationId: number | undefined - ID of the conversation to continue (optional)
- userId: string - The authenticated user's ID

**Returns:**
- Promise resolving to:
```json
{
  "conversation_id": 123,
  "response": "Task added: Buy groceries",
  "tool_calls": []
}
```

**Errors:**
- Network errors: Throw appropriate error for UI handling
- Backend errors: Return error object with message

## Type Definitions

### TypeScript Interfaces

```typescript
interface ChatRequest {
  conversation_id?: number;
  message: string;
}

interface ChatResponse {
  conversation_id: number;
  response: string;
  tool_calls?: any[];
}

interface SendMessageParams {
  message: string;
  conversationId?: number;
  userId: string;
}
```