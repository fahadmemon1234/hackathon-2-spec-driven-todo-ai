# Qwen Agent Context: AI-Powered Chatbot for Task Management

## Feature Overview
The AI-Powered Chatbot for Task Management feature transforms the existing full-stack todo app into an AI-agentic application where users manage tasks entirely through natural language using an OpenAI agent powered by MCP tools.

## Key Components
1. **MCP Server**: Implements the Model Context Protocol to expose task operations as tools for the AI agent
2. **Chat Endpoint**: Orchestrates conversation flow, history management, and agent execution
3. **Database**: Extended with Conversation and Message models to store chat history
4. **Frontend**: OpenAI ChatKit integration for a natural chat interface

## MCP Tools Available
- `add_task`: Create new tasks
- `list_tasks`: Retrieve user's tasks with optional filtering
- `update_task`: Modify task title or description
- `complete_task`: Mark tasks as completed
- `delete_task`: Remove tasks

## Implementation Notes
- MCP server uses FastMCP to integrate with FastAPI
- Authentication enforced via Better Auth JWT tokens
- Conversation history persisted in database for continuity
- OpenAI Agent instantiated per request for proper isolation
- Frontend connects directly to custom backend endpoint

## Architecture
- Backend: FastAPI + SQLModel + Better Auth
- Frontend: Next.js + OpenAI ChatKit
- Database: Neon DB with extended schema
- AI Integration: OpenAI Agents SDK + MCP tools

## Important Files
- `backend/mcp_server.py`: MCP server implementation
- `backend/routes/chat.py`: Chat endpoint implementation
- `backend/models.py`: Extended data models with Conversation and Message
- `frontend/app/chat/page.tsx`: Chat interface implementation

## Environment Variables
- OPENAI_API_KEY: Required for OpenAI integration
- NEXT_PUBLIC_OPENAI_DOMAIN_KEY: Required for production ChatKit usage

## Domain Allowlist (Production)
For production deployments, add your domain to OpenAI's domain allowlist at:
https://platform.openai.com/settings/organization/security/domain-allowlist