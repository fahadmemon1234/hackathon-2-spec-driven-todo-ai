---
id: 6
title: mcp-server-fix
stage: green
date: 2026-01-06
surface: agent
model: Qwen
feature: ai-chatbot-task-management
branch: 14-ai-chatbot-task-management
user: user
command: manual-fix
labels: ["backend", "mcp", "api", "fix"]
links:
  spec: "F:\\Programing\\governor Inititative Program IT\\Ai\\Hackathon 2\\todo-app-Phase-3\\specs\\14-ai-chatbot-task-management\\spec.md"
  plan: "F:\\Programing\\governor Inititative Program IT\\Ai\\Hackathon 2\\todo-app-Phase-3\\specs\\14-ai-chatbot-task-management\\plan.md"
  tasks: "F:\\Programing\\governor Inititative Program IT\\Ai\\Hackathon 2\\todo-app-Phase-3\\specs\\14-ai-chatbot-task-management\\tasks.md"
  ticket: null
  adr: null
  pr: null
files:
 - "F:\\Programing\\governor Inititative Program IT\\Ai\\Hackathon 2\\todo-app-Phase-3\\backend\\mcp_server.py"
 - "F:\\Programing\\governor Inititative Program IT\\Ai\\Hackathon 2\\todo-app-Phase-3\\backend\\main.py"
tests:
 - "backend/mcp_server.py"
---

## Prompt

Fix the MCP server implementation that was causing AttributeError: module 'mcp.types' has no attribute 'ToolParameterInfo'

## Response snapshot

Successfully fixed the MCP server implementation by:
- Removing incorrect type annotations (ToolParameterInfo, ToolResultInfo) that don't exist in the MCP library
- Simplifying function signatures to use basic type hints instead of MCP-specific annotations
- Removing unused imports (types, Annotated)
- Clearing Python cache files to ensure the updated module is loaded
- Verifying that all MCP tool functions have correct signatures compatible with the MCP library

The MCP server now properly defines the five required tools (add_task, list_tasks, update_task, complete_task, delete_task) with correct function signatures that the MCP library can process without errors.

## Outcome

- ✅ Impact: Fixed MCP server runtime error and enabled proper tool functionality
- 🧪 Tests: Verified module imports and function signatures
- 📁 Files: 1 file updated with corrected MCP server implementation
- 🔁 Next prompts: Ready for OpenAI Agents integration
- 🧠 Reflection: Implementation now follows MCP library requirements correctly

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Test MCP server with OpenAI Agents