# Feature Specification: Single Task Operations

**Feature Branch**: `9-single-task-ops`
**Created**: 2025-01-07
**Status**: Draft
**Input**: User description: "# Task 5: Single Task Operations Specification + Implementation # Phase II Backend – Implement GET, PUT, DELETE, PATCH for /api/tasks/{id} # Current Status: Task 1-4 complete (Create & List working with user isolation) You are an expert FastAPI developer specializing in secure CRUD operations. Goal for Task 5: Implement the remaining four endpoints for individual task operations: - GET /api/tasks/{id} → Retrieve single task - PUT /api/tasks/{id} → Full update (title and/or description) - DELETE /api/tasks/{id} → Delete task - PATCH /api/tasks/{id}/complete → Toggle completion status All operations MUST enforce strict ownership: only the task owner can access/modify. Requirements: 1. Add to routes/tasks.py (existing router with prefix="/api") 2. Common Helper (optional but recommended) - Create a private function to fetch task with ownership check: def get_task_or_404(id: int, user_id: str, session: Session) -> Task: task = session.get(Task, id) if not task: raise HTTPException(status_code=404, detail="Task not found") if task.user_id != user_id: raise HTTPException(status_code=403, detail="Not authorized to access this task") return task 3. GET /api/tasks/{id} – Retrieve Single Task @router.get("/tasks/{id}", response_model=Task) def get_task( id: int, user_id: str = Depends(get_current_user_id), session: Session = Depends(get_session) ): task = get_task_or_404(id, user_id, session) return task 4. PUT /api/tasks/{id} – Update Task - Request body model: class TaskUpdate(SQLModel): title: Optional[str] = Field(default=None, min_length=1, max_length=200) description: Optional[str] = Field(default=None, max_length=1000) @router.put("/tasks/{id}", response_model=Task) def update_task( id: int, task_data: TaskUpdate, user_id: str = Depends(get_current_user_id), session: Session = Depends(get_session) ): task = get_task_or_404(id, user_id, session) if task_data.title is not None: task.title = task_data.title if task_data.description is not None: task.description = task_data.description session.add(task) session.commit() session.refresh(task) return task 5. DELETE /api/tasks/{id} – Delete Task @router.delete("/tasks/{id}", status_code=204) def delete_task( id: int, user_id: str = Depends(get_current_user_id), session: Session = Depends(get_session) ): task = get_task_or_404(id, user_id, session) session.delete(task) session.commit() return Response(status_code=204) 6. PATCH /api/tasks/{id}/complete – Toggle Completion @router.patch("/tasks/{id}/complete", response_model=Task) def toggle_complete( id: int, user_id: str = Depends(get_current_user_id), session: Session = Depends(get_session) ): task = get_task_or_404(id, user_id, session) task.completed = not task.completed session.add(task) session.commit() session.refresh(task) return task 7. Expected Behavior - All endpoints require valid JWT → 401 if missing/invalid - Wrong task ID → 404 - Task belongs to another user → 403 Forbidden - Successful operations return correct status and data - updated_at automatically updated on modifications (from model definition) Refer to: @specs/features/task-crud.md @specs/api/rest-endpoints.md @backend/CLAUDE.md Now implement Task 5 exactly as specified. Add the four endpoints to routes/tasks.py. Use the helper function for clean, DRY code. Ensure full ownership enforcement on every operation. After this task, all 5 basic CRUD features will be complete and secure."
**Constitution Compliance**: All features must adhere to project constitution principles

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Retrieve Individual Tasks (Priority: P1)

An authenticated user wants to view details of a specific task from their collection. The user selects a task from the list view and expects to see its complete details.

**Why this priority**: This is essential functionality that allows users to view detailed information about specific tasks, which is necessary for effective task management.

**Independent Test**: Can be fully tested by sending authenticated GET requests to /api/tasks/{id} and verifying that users can only retrieve their own tasks, delivering the core value of detailed task access.

**Acceptance Scenarios**:

1. **Given** a user has created tasks, **When** they send a GET request to /api/tasks/{valid_id}, **Then** they receive the complete task details
2. **Given** a user tries to access a non-existent task ID, **When** they send a GET request to /api/tasks/{invalid_id}, **Then** a 404 Not Found response is returned
3. **Given** a user tries to access a task that belongs to another user, **When** they send a GET request to that task's ID, **Then** a 403 Forbidden response is returned
4. **Given** a user sends a request without a valid JWT token, **When** they try to retrieve a task, **Then** a 401 Unauthorized response is returned

---

### User Story 2 - Update Task Details (Priority: P1)

An authenticated user wants to modify the details of an existing task (title or description). The user makes changes to a task and expects those changes to be saved and reflected in the system.

**Why this priority**: This is fundamental functionality that allows users to keep their task information up-to-date, which is essential for effective task management.

**Independent Test**: Can be fully tested by sending authenticated PUT requests to /api/tasks/{id} with updated task data and verifying that only the task owner can update their tasks, delivering the core value of task modification.

**Acceptance Scenarios**:

1. **Given** a user owns a task, **When** they send a PUT request to /api/tasks/{id} with new title/description, **Then** the task is updated with new values
2. **Given** a user tries to update a non-existent task ID, **When** they send a PUT request, **Then** a 404 Not Found response is returned
3. **Given** a user tries to update a task that belongs to another user, **When** they send a PUT request, **Then** a 403 Forbidden response is returned
4. **Given** a user sends invalid data (empty title), **When** they send a PUT request, **Then** a 422 Validation Error response is returned

---

### User Story 3 - Delete Tasks (Priority: P1)

An authenticated user wants to remove tasks they no longer need. The user selects a task for deletion and expects it to be permanently removed from their collection.

**Why this priority**: This is essential functionality that allows users to clean up their task lists and remove obsolete items, which is critical for maintaining an organized todo system.

**Independent Test**: Can be fully tested by sending authenticated DELETE requests to /api/tasks/{id} and verifying that only the task owner can delete their tasks, delivering the core value of task removal.

**Acceptance Scenarios**:

1. **Given** a user owns a task, **When** they send a DELETE request to /api/tasks/{id}, **Then** the task is permanently removed and a 204 No Content response is returned
2. **Given** a user tries to delete a non-existent task ID, **When** they send a DELETE request, **Then** a 404 Not Found response is returned
3. **Given** a user tries to delete a task that belongs to another user, **When** they send a DELETE request, **Then** a 403 Forbidden response is returned
4. **Given** a user sends a request without a valid JWT token, **When** they try to delete a task, **Then** a 401 Unauthorized response is returned

---

### User Story 4 - Toggle Task Completion (Priority: P1)

An authenticated user wants to mark tasks as complete or incomplete. The user toggles the completion status of a task and expects the system to update this status appropriately.

**Why this priority**: This is core functionality that allows users to track their progress and mark completed tasks, which is fundamental to a todo application's purpose.

**Independent Test**: Can be fully tested by sending authenticated PATCH requests to /api/tasks/{id}/complete and verifying that only the task owner can toggle completion status, delivering the core value of task status management.

**Acceptance Scenarios**:

1. **Given** a user owns a pending task, **When** they send a PATCH request to /api/tasks/{id}/complete, **Then** the task's completion status changes to completed
2. **Given** a user owns a completed task, **When** they send a PATCH request to /api/tasks/{id}/complete, **Then** the task's completion status changes to pending
3. **Given** a user tries to toggle completion of a non-existent task ID, **When** they send a PATCH request, **Then** a 404 Not Found response is returned
4. **Given** a user tries to toggle completion of a task that belongs to another user, **When** they send a PATCH request, **Then** a 403 Forbidden response is returned

---

### Edge Cases

- What happens when a user tries to update a task with extremely long title or description?
- How does the system handle concurrent updates to the same task by the same user?
- What occurs when the database is temporarily unavailable during an operation?
- How does the system handle malformed request bodies during update operations?
- What happens when a user tries to perform operations on a task that was deleted by another request?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide GET /api/tasks/{id} endpoint to retrieve individual tasks
- **FR-002**: System MUST provide PUT /api/tasks/{id} endpoint to update task details (title and/or description)
- **FR-003**: System MUST provide DELETE /api/tasks/{id} endpoint to remove tasks
- **FR-004**: System MUST provide PATCH /api/tasks/{id}/complete endpoint to toggle completion status
- **FR-005**: System MUST enforce authentication on all endpoints (401 for invalid/missing JWT)
- **FR-006**: System MUST enforce ownership validation (403 if task doesn't belong to user)
- **FR-007**: System MUST return 404 for non-existent task IDs
- **FR-008**: System MUST validate input data (title: 1-200 chars, description: 0-1000 chars)
- **FR-009**: System MUST update the updated_at timestamp automatically on modifications
- **FR-010**: System MUST return appropriate HTTP status codes (200/204 for success, 401/403/404 for errors)
- **FR-011**: System MUST return complete task object after successful PUT/PATCH operations
- **FR-012**: System MUST implement proper error handling with informative but secure error messages
- **FR-013**: System MUST use helper functions to avoid code duplication in ownership checks
- **FR-014**: System MUST accept optional title and description in PUT requests
- **FR-015**: System MUST return 204 No Content for successful DELETE operations

### Key Entities

- **Individual Task Operation**: Represents a single task CRUD operation (GET, PUT, DELETE, PATCH) with proper authentication and authorization
- **Task Update Request**: Represents the data needed to update a task (optional title, optional description) with validation constraints
- **Task Ownership**: Represents the relationship between a user and their tasks, ensuring only owners can access/modify their tasks
- **Task Completion Toggle**: Represents the operation to switch a task's completion status between pending and completed

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can retrieve individual tasks with 99.9% success rate when authorized
- **SC-002**: Users can update task details with 99.8% success rate when authorized and providing valid data
- **SC-003**: Users can delete their tasks with 99.9% success rate when authorized
- **SC-004**: Users can toggle task completion status with 99.9% success rate when authorized
- **SC-005**: Unauthorized access attempts are properly blocked with 100% accuracy
- **SC-006**: All endpoints respond within 200ms for 95% of requests under normal load
- **SC-007**: Task ownership enforcement prevents unauthorized access with 100% effectiveness
- **SC-008**: Input validation prevents invalid data with 100% accuracy
- **SC-009**: All 5 basic CRUD features (Create, Read, Update, Delete, Toggle Complete) are fully implemented
- **SC-010**: The system handles 1000 concurrent authenticated users performing individual task operations without degradation