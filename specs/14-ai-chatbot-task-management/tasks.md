# Tasks: AI-Powered Chatbot for Task Management

**Feature**: 14-ai-chatbot-task-management
**Created**: 2026-01-06
**Status**: Draft

## Phase 1: Setup

- [X] T001 Create feature branch 14-ai-chatbot-task-management
- [X] T002 Install new dependencies: mcp[fastapi] and openai-agents in backend
- [X] T003 Install new dependency: @openai/chatkit in frontend
- [X] T004 Verify existing project structure and dependencies

## Phase 2: Foundational Tasks

- [X] T005 [P] Add Conversation model to backend/models.py based on data model design
- [X] T006 [P] Add Message model to backend/models.py based on data model design
- [X] T007 Create database migration script for conversations and messages tables
- [X] T008 Run database migration to create conversations and messages tables
- [X] T009 Verify database schema matches design specifications

## Phase 3: User Story 1 - Natural Language Task Management (Priority: P1)

- [X] T010 [US1] Create mcp_server.py file with FastMCP initialization
- [X] T011 [US1] Implement add_task MCP tool with user_id validation and ownership enforcement
- [X] T012 [US1] Implement list_tasks MCP tool with status filtering and user_id validation
- [X] T013 [US1] Implement update_task MCP tool with user_id validation and ownership enforcement
- [X] T014 [US1] Implement complete_task MCP tool with user_id validation and ownership enforcement
- [X] T015 [US1] Implement delete_task MCP tool with user_id validation and ownership enforcement
- [ ] T016 [US1] Test MCP tools independently using test scripts
- [X] T017 [US1] Create POST /api/{user_id}/chat endpoint in backend/routes/chat.py
- [X] T018 [US1] Implement conversation management (create/load) in chat endpoint
- [X] T019 [US1] Implement storing user message in messages table
- [X] T020 [US1] Implement loading full conversation history
- [X] T021 [US1] Configure OpenAI Agent with system prompt and MCP tools
- [X] T022 [US1] Implement agent execution and capture response + tool calls
- [X] T023 [US1] Store assistant response as new message
- [X] T024 [US1] Return conversation_id and response to frontend
- [ ] T025 [US1] Test natural language task creation: "Add a task to buy milk tomorrow"
- [ ] T026 [US1] Test natural language task listing: "Show my pending tasks"
- [ ] T027 [US1] Test natural language task completion: "Mark the groceries task as done"
- [ ] T028 [US1] Test natural language task deletion: "Delete task 5"

## Phase 4: User Story 2 - Conversation Continuity (Priority: P2)

- [ ] T029 [US2] Enhance conversation loading to include full history context
- [ ] T030 [US2] Test conversation resumption functionality
- [ ] T031 [US2] Test AI's ability to reference previous tasks in conversation
- [ ] T032 [US2] Verify conversation history persists across server restarts

## Phase 5: User Story 3 - Friendly AI Responses (Priority: P3)

- [ ] T033 [US3] Update system prompt to ensure friendly confirmation messages
- [ ] T034 [US3] Test successful operation confirmations (e.g., "Task added: Buy groceries!")
- [ ] T035 [US3] Test error message handling (e.g., "No task found with ID 3")
- [ ] T036 [US3] Verify all AI responses are user-friendly and helpful

## Phase 6: User Story 4 - Ambiguous Request Handling (Priority: P3)

- [ ] T037 [US4] Implement disambiguation logic for requests with multiple possible matches
- [ ] T038 [US4] Test ambiguous request handling: "delete the groceries task" when multiple exist
- [ ] T039 [US4] Verify AI asks for clarification rather than making incorrect assumptions

## Phase 7: Frontend Integration

- [X] T040 Create chat page/route at frontend/app/chat/page.tsx
- [X] T041 Integrate OpenAI ChatKit component in the chat page
- [X] T042 Connect ChatKit to custom /api/{user_id}/chat backend endpoint
- [X] T043 Implement conversation_id handling (new/resume)
- [X] T044 Add loading states during agent thinking/tool calls
- [X] T045 Style chat interface with Tailwind to match existing theme
- [X] T046 Test end-to-end flow from frontend to backend

## Phase 8: Polish & Cross-Cutting Concerns

- [X] T047 Handle authentication errors (401 responses) gracefully
- [ ] T048 Handle conversation not found errors (404 responses) gracefully
- [ ] T049 Handle agent execution failures (500 responses) gracefully
- [ ] T050 Add domain allowlist setup instructions to README
- [ ] T051 Update documentation with new environment variables
- [ ] T052 Perform end-to-end testing of all user stories
- [ ] T053 Verify all success criteria are met

## Dependencies

- User Story 2 depends on foundational database tasks (T005-T009) being completed
- User Story 3 and 4 depend on User Story 1 being completed
- Frontend Integration depends on User Story 1 being completed
- Polish phase depends on all user stories being completed

## Parallel Execution Examples

- T005 and T006 can run in parallel (adding models)
- T011-T015 can run in parallel (implementing MCP tools)
- T029-T032 can run in parallel (testing conversation continuity)
- T033-T036 can run in parallel (testing friendly responses)

## Implementation Strategy

1. **MVP Scope**: Complete Phase 1, 2, and Phase 3 (User Story 1) to achieve minimum viable product
2. **Incremental Delivery**: Each user story builds upon the previous to provide continuous value
3. **Testing**: Each phase includes specific test scenarios to validate functionality
4. **Quality Assurance**: Final phase includes comprehensive testing of all success criteria