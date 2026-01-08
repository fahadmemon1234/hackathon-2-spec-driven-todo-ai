# Implementation Plan: AI-Powered Chatbot for Task Management

**Feature**: 14-ai-chatbot-task-management
**Created**: 2026-01-06
**Status**: Draft
**Constitution Compliance**: All implementations must adhere to project constitution principles

## Technical Context

- **Backend Framework**: FastAPI (existing in project)
- **Database**: SQLModel with Neon DB (existing in project)
- **Authentication**: Better Auth JWT (existing in project)
- **Frontend**: Next.js with Tailwind (existing in project)
- **AI Integration**: OpenAI Agents SDK with Model Context Protocol (MCP) tools
- **Chat Interface**: OpenAI ChatKit
- **Environment**: Python 3.13+, Node.js 20+

### Dependencies to Install
- `mcp[fastapi]` - Official MCP Python SDK with FastMCP
- `openai-agents` - OpenAI Agents Python SDK
- `@openai/chatkit` - OpenAI ChatKit for frontend

### Integration Points
- **Existing Task API**: MCP tools will reuse existing task models and database operations
- **Authentication System**: Leverage existing Better Auth JWT implementation
- **Database Schema**: Extend with Conversation and Message models
- **Frontend Structure**: Add new chat page/route to existing Next.js app

### Architecture Overview
- MCP Server: Exposes task operations as tools for the AI agent
- Chat Endpoint: Orchestrates conversation flow, history management, and agent execution
- Database: Stores conversations and messages in addition to existing tasks
- Frontend: Provides chat interface connecting to backend endpoint

### Known Unknowns
- Specific configuration details for MCP server transport protocol
- Exact format for OpenAI agent system prompt integration
- ChatKit client token generation requirements (if any)

## Constitution Check

- ✅ **AI-Centric Development**: Plan relies on AI tools for implementation (Claude Code for primary implementation, Qwen for planning)
- ✅ **Spec-Driven Approach**: Implementation follows formal specification in spec.md
- ✅ **Clean Code and Modularity**: Plan separates concerns (MCP server, chat endpoint, frontend)
- ✅ **Transparency and Iteration**: All steps documented for traceability
- ✅ **Scalability Focus**: Design considers persistent storage and user isolation
- ✅ **Ethical AI Use**: Plan includes error handling and user data protection

## Gates (Block on FAIL)

- ✅ **Technical Feasibility**: All required technologies (MCP SDK, OpenAI Agents, ChatKit) are officially available
- ✅ **Architecture Alignment**: Solution fits within existing tech stack (FastAPI, NextJS, SQLModel)
- ✅ **Security Compliance**: Authentication and user isolation maintained via JWT
- ✅ **Performance Impact**: Stateless design preserves system responsiveness
- ✅ **Dependency Management**: All dependencies can be added via standard package managers

## Phase 0: Research & Resolution

### Research Tasks

#### RT-001: MCP Server Configuration
- **Decision**: Determine optimal transport protocol for MCP server integration with FastAPI
- **Rationale**: Need to select between available transport options (HTTP, SSE, WebSocket)
- **Alternatives considered**: HTTP endpoints, Server-Sent Events, WebSocket connections

#### RT-002: OpenAI Agent Integration Patterns
- **Decision**: Determine best practice for integrating OpenAI Agents SDK with FastAPI endpoint
- **Rationale**: Need to understand how to properly instantiate and run agents in request context
- **Alternatives considered**: Per-request instantiation vs. shared agent instance vs. agent pool

#### RT-003: ChatKit Authentication Strategy
- **Decision**: Determine how to handle authentication between ChatKit frontend and custom backend
- **Rationale**: Need to ensure secure connection between chat interface and our API
- **Alternatives considered**: Client token generation, direct backend connection, proxy approach

## Phase 1: Design & Contracts

### Data Model Design

#### Conversation Model
- **id**: integer (primary key, auto-increment)
- **user_id**: string (foreign key to users table, enforces ownership)
- **created_at**: datetime (timestamp when conversation started)
- **updated_at**: datetime (timestamp of last activity)

#### Message Model
- **id**: integer (primary key, auto-increment)
- **conversation_id**: integer (foreign key to conversations table)
- **role**: string (enum: "user" | "assistant", determines message origin)
- **content**: text (the actual message content)
- **created_at**: datetime (timestamp when message was created)

#### Relationships
- Conversation (1) → Messages (Many): One conversation contains many messages
- User (1) → Conversations (Many): One user can have multiple conversations

### API Contract Design

#### POST /api/{user_id}/chat
- **Authentication**: JWT token required, user_id in path must match token
- **Request Body**:
  ```json
  {
    "conversation_id": "integer (optional - creates new if absent)",
    "message": "string (required - user's natural language input)"
  }
  ```
- **Response**:
  ```json
  {
    "conversation_id": "integer",
    "response": "string (AI's natural language response)",
    "tool_calls": "array (optional - for debugging/transparency)"
  }
  ```
- **Error Codes**:
  - 401: Unauthorized (invalid/missing JWT)
  - 404: Not Found (conversation_id doesn't exist or not owned by user)
  - 500: Internal Server Error (agent execution failed)

#### MCP Tools API (Internal)
The following tools will be available internally to the OpenAI agent:

##### add_task
- **Purpose**: Create a new task
- **Parameters**: 
  - user_id: string (authenticated user)
  - title: string (required, 1-200 chars)
  - description: string (optional, max 1000 chars)
- **Returns**: {"task_id": int, "status": "created", "title": string, "description": string or null}

##### list_tasks
- **Purpose**: List tasks for the user
- **Parameters**:
  - user_id: string (required)
  - status: string (optional: "all" | "pending" | "completed", default "all")
- **Returns**: Array of {"id": int, "title": string, "description": string or null, "completed": bool, "created_at": timestamp}

##### update_task
- **Purpose**: Update task title/description
- **Parameters**:
  - user_id: string (required)
  - task_id: int (required)
  - title: string (optional)
  - description: string (optional)
- **Returns**: {"task_id": int, "status": "updated", "title": string}

##### complete_task
- **Purpose**: Toggle task completion (mark as complete)
- **Parameters**:
  - user_id: string (required)
  - task_id: int (required)
- **Returns**: {"task_id": int, "status": "completed", "title": string}

##### delete_task
- **Purpose**: Delete a task
- **Parameters**:
  - user_id: string (required)
  - task_id: int (required)
- **Returns**: {"task_id": int, "status": "deleted", "title": string}

### Quickstart Guide

1. **Setup Environment**:
   ```bash
   # Install new dependencies
   pip install mcp[fastapi] openai-agents
   cd frontend && npm install @openai/chatkit
   ```

2. **Database Migrations**:
   ```bash
   # Run migrations to add Conversation and Message tables
   python -m backend.database.migrate
   ```

3. **Start Services**:
   ```bash
   # Start backend (includes MCP server)
   uvicorn backend.main:app --reload

   # In another terminal, start frontend
   cd frontend && npm run dev
   ```

4. **Access Chat Interface**:
   - Navigate to http://localhost:3000/chat
   - Login with existing credentials
   - Start chatting with the AI assistant

### Agent Context Update
- Qwen agent context has been updated with relevant information about the AI chatbot feature
- Key information about MCP tools, architecture, and implementation notes are available to the AI

## Phase 2: Implementation Strategy

### Implementation Order (Recommended Sequence)

#### Phase 2A: Database Extensions
1. Add Conversation and Message models to existing models.py
2. Create and run database migration
3. Verify data persistence works correctly

#### Phase 2B: MCP Server & Tools
1. Install and set up official MCP Python SDK
2. Implement all 5 MCP tools (add_task, list_tasks, update_task, complete_task, delete_task)
3. Enforce user ownership using authenticated user_id
4. Test tools independently

#### Phase 2C: Chat Endpoint & Agent Integration
1. Implement POST /api/{user_id}/chat endpoint
2. Add conversation management (create/load)
3. Store user message
4. Load full history
5. Configure OpenAI Agent with system prompt and MCP tools
6. Run agent → capture response + tool calls
7. Store assistant message
8. Return response to frontend

#### Phase 2D: Frontend Chat Interface
1. Install and configure OpenAI ChatKit
2. Create chat page/route
3. Connect to custom /api/{user_id}/chat endpoint
4. Handle conversation_id (new/resume)
5. Add loading states and nice formatting
6. Test end-to-end flow

#### Phase 2E: Polish & Testing
1. Improve agent responses (confirmations, lists formatting)
2. Handle edge cases (task not found, ambiguity)
3. Add domain allowlist + production env setup
4. Update documentation

## Risk Assessment

- **High Risk**: MCP server integration complexity
  - *Mitigation*: Thorough testing of each tool individually before integration
  
- **Medium Risk**: OpenAI agent response quality
  - *Mitigation*: Comprehensive system prompt and fallback error handling
  
- **Medium Risk**: Authentication flow with ChatKit
  - *Mitigation*: Clear separation of authentication concerns and proper error handling

## Success Criteria Verification

At the end of implementation:
- [ ] Users can create tasks via natural language chat
- [ ] Users can list, update, complete, and delete tasks via chat
- [ ] Conversation history persists across sessions
- [ ] Authentication properly enforces user isolation
- [ ] AI provides helpful, contextual responses
- [ ] System handles errors gracefully with user-friendly messages