# Research Findings: AI-Powered Chatbot for Task Management

**Feature**: 14-ai-chatbot-task-management
**Created**: 2026-01-06
**Status**: Completed

## RT-001: MCP Server Configuration

### Decision
Use HTTP transport for MCP server integration with FastAPI, specifically mounting the MCP router as a sub-application within the main FastAPI application.

### Rationale
HTTP transport is the most straightforward approach for integrating MCP server with FastAPI. The FastMCP library provides a router that can be directly included in the main FastAPI application, making it accessible under a specific path prefix (e.g., /mcp). This approach is well-documented and aligns with standard FastAPI practices.

### Alternatives considered
- **Server-Sent Events (SSE)**: More complex to implement and maintain, typically used for streaming data
- **WebSocket connections**: Overkill for tool-based interactions, adds complexity for bidirectional communication that isn't needed
- **Direct HTTP endpoints**: Would require manual implementation of MCP protocol, defeating the purpose of using the SDK

## RT-002: OpenAI Agent Integration Patterns

### Decision
Use per-request instantiation of the OpenAI Agent within the chat endpoint, creating a fresh agent instance for each conversation request.

### Rationale
Per-request instantiation ensures proper isolation between different user requests and conversations. It avoids potential state contamination between requests and simplifies resource management. Since the agent execution is typically short-lived (seconds), the overhead of creating a new instance per request is acceptable.

### Alternatives considered
- **Shared agent instance**: Could lead to state contamination and security issues between different users
- **Agent pool**: Adds complexity without significant benefits for this use case, as agent execution is not a long-running process

## RT-003: ChatKit Authentication Strategy

### Decision
Implement direct backend connection approach where ChatKit communicates with our custom /api/{user_id}/chat endpoint, leveraging existing Better Auth JWT for authentication.

### Rationale
The direct backend connection approach maintains consistency with existing authentication patterns in the application. It avoids the complexity of managing ChatKit-specific client tokens while ensuring that all requests go through our established authentication middleware. This approach also gives us full control over the conversation flow and data.

### Alternatives considered
- **Client token generation**: Would require additional infrastructure and doesn't align with existing authentication patterns
- **Proxy approach**: Adds unnecessary complexity and potential points of failure

## Additional Research: OpenAI Agent System Prompt Integration

### Decision
Pass the system prompt directly to the Agent constructor as a string constant, following the exact prompt specified in the feature requirements.

### Rationale
The OpenAI Agents SDK allows specifying the system prompt during agent creation. Using the exact prompt from the feature specification ensures consistent behavior and meets the requirements. Storing it as a constant in the code keeps it version-controlled and easily modifiable.

## Additional Research: Database Migration Strategy

### Decision
Use SQLModel's migration capabilities combined with Alembic for database schema evolution, adding the new Conversation and Message models to the existing migration workflow.

### Rationale
SQLModel works well with Alembic for database migrations, and this approach maintains consistency with existing database management practices in the project. It allows for proper versioning of schema changes and supports both forward and rollback operations.

## Additional Research: Error Handling in MCP Tools

### Decision
Implement consistent error handling in all MCP tools that catches exceptions and returns appropriate error responses that the OpenAI agent can interpret.

### Rationale
Proper error handling ensures that when issues occur (e.g., database connectivity problems, invalid inputs), the agent receives structured error responses rather than unhandled exceptions. This enables graceful degradation and better user experience.