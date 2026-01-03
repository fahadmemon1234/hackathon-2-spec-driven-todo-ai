# Feature Specification: Backend API Enhancement

**Feature Branch**: `11-backend-api-enhancement`
**Created**: 2025-01-07
**Status**: Draft
**Input**: User description: "# Task 2: Update Backend API – Create/Update + Enhanced List Specification + Implementation # Phase II Intermediate Level – Backend Changes for Priorities, Categories, Search, Filter & Sort # Current Status: Task 1 complete (priority & category fields added to Task model & DB) You are an expert FastAPI + SQLModel developer. Goal for Task 2: Update the backend API to fully support Intermediate Level features: - Accept priority & category on create/update - Enhanced GET /api/tasks with new query params: search, priority, category, extended sort Requirements: 1. Update Pydantic Models in routes/tasks.py - TaskCreate: class TaskCreate(SQLModel): title: str = Field(min_length=1, max_length=200) description: Optional[str] = Field(default=None, max_length=1000) priority: Optional[str] = Field(default="medium", regex="^(high|medium|low)$") category: Optional[str] = Field(default=None, max_length=50) - TaskUpdate: class TaskUpdate(SQLModel): title: Optional[str] = Field(default=None, min_length=1, max_length=200) description: Optional[str] = Field(default=None, max_length=1000) priority: Optional[str] = Field(default=None, regex="^(high|medium|low)$") category: Optional[str] = Field(default=None, max_length=50) 2. Update POST /tasks and PUT /tasks/{id} - In create_task and update_task: - Accept and save priority and category from request body - Default priority="medium" if not provided - Allow null/empty category 3. Enhance GET /api/tasks – Advanced Query Support @router.get("/tasks", response_model=List[Task]) def list_tasks( user_id: str = Depends(get_current_user_id), status: Optional[str] = Query(None), priority: Optional[str] = Query(None, regex="^(high|medium|low)$"), category: Optional[str] = Query(None), search: Optional[str] = Query(None), sort: Optional[str] = Query("created", regex="^(created|title|priority|category)$"), session: Session = Depends(get_session) ): statement = select(Task).where(Task.user_id == user_id) # Status filter if status == "pending": statement = statement.where(Task.completed == False) elif status == "completed": statement = statement.where(Task.completed == True) # Priority filter if priority: statement = statement.where(Task.priority == priority) # Category filter if category: statement = statement.where(Task.category == category) # Search in title or description if search: search_term = f"%{search.lower()}%" statement = statement.where( or_( Task.title.ilike(search_term), Task.description.ilike(search_term) ) ) # Sorting if sort == "title": statement = statement.order_by(Task.title.asc()) elif sort == "priority": # High > Medium > Low statement = statement.order_by( case( (Task.priority == "high", 1), (Task.priority == "medium", 2), (Task.priority == "low", 3), ), Task.created_at.desc() ) elif sort == "category": statement = statement.order_by(Task.category.asc(), Task.created_at.desc()) else: # created (default newest first) statement = statement.order_by(Task.created_at.desc()) tasks = session.exec(statement).all() return tasks 4. Required Imports - from sqlalchemy import or_, case 5. Expected Behavior - Create task with priority="high" and category="work" → saved correctly - Update task → can change priority/category - GET /api/tasks?priority=high → only high priority - GET /api/tasks?category=work → only work category - GET /api/tasks?search=buy → matches title or description - GET /api/tasks?sort=priority → high first, then medium, then low - All filters combinable - Invalid param → 422 validation error Refer to: @specs/api/rest-endpoints.md (update GET params) @backend/CLAUDE.md Now implement Task 2 exactly as specified. Update routes/tasks.py with new models, updated create/update logic, and enhanced GET endpoint with full search, filter, and sort support. Ensure backward compatibility (old requests without new fields still work). After this task, backend will fully support Intermediate Level data and querying."
**Constitution Compliance**: All features must adhere to project constitution principles

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Enhanced Task Creation (Priority: P1)

An authenticated user wants to create tasks with additional organizational information like priority level and category. The user provides task details through the frontend which sends a POST request to the backend API with priority and category information.

**Why this priority**: This is the foundational functionality that allows users to add richer organizational context to their tasks, which is essential for effective task management.

**Independent Test**: Can be fully tested by sending authenticated POST requests to /api/tasks with priority and category data and verifying that tasks are created with the correct additional information, delivering the core value of enhanced task creation.

**Acceptance Scenarios**:

1. **Given** a user is authenticated with a valid JWT token, **When** they send a POST request to /api/tasks with priority and category, **Then** a new task is created with the specified priority and category
2. **Given** a user sends a POST request without priority, **When** they create a task, **Then** the task is created with default "medium" priority
3. **Given** a user sends a POST request without category, **When** they create a task, **Then** the task is created with null category
4. **Given** a user provides invalid priority value, **When** they create a task, **Then** a 422 validation error is returned

---

### User Story 2 - Enhanced Task Updates (Priority: P1)

An authenticated user wants to update their existing tasks with new priority or category information. The user modifies task details through the frontend which sends a PUT request to update the task with new organizational information.

**Why this priority**: This enables users to reorganize and reprioritize their tasks as circumstances change, which is essential for effective task management.

**Independent Test**: Can be fully tested by sending authenticated PUT requests to /api/tasks/{id} with updated priority and category data and verifying that tasks are updated correctly, delivering the core value of flexible task management.

**Acceptance Scenarios**:

1. **Given** a user has a task, **When** they send a PUT request to /api/tasks/{id} with new priority/category, **Then** the task is updated with the new values
2. **Given** a user updates only priority, **When** they send a PUT request, **Then** only priority changes, other fields remain unchanged
3. **Given** a user updates only category, **When** they send a PUT request, **Then** only category changes, other fields remain unchanged
4. **Given** a user provides invalid priority value, **When** they update a task, **Then** a 422 validation error is returned

---

### User Story 3 - Advanced Task Filtering and Searching (Priority: P1)

An authenticated user with many tasks wants to find specific tasks quickly using search and filter capabilities. The user sends GET requests to /api/tasks with query parameters to narrow down their task list.

**Why this priority**: This significantly improves usability when managing a large number of tasks, making the application more efficient for daily use.

**Independent Test**: Can be fully tested by creating tasks with various attributes, then using query parameters to filter and search, verifying that only matching tasks are returned, delivering the core value of efficient task discovery.

**Acceptance Scenarios**:

1. **Given** a user has tasks with different priorities, **When** they request /api/tasks?priority=high, **Then** only high priority tasks are returned
2. **Given** a user has tasks in different categories, **When** they request /api/tasks?category=work, **Then** only work category tasks are returned
3. **Given** a user has tasks with various titles/descriptions, **When** they request /api/tasks?search=meeting, **Then** tasks containing "meeting" in title or description are returned
4. **Given** a user combines multiple filters, **When** they request /api/tasks?status=pending&priority=high, **Then** only pending high priority tasks are returned

---

### User Story 4 - Advanced Task Sorting (Priority: P2)

An authenticated user wants to view their tasks in different orders to better organize their workflow. The user sends GET requests to /api/tasks with sort parameters to order their task list.

**Why this priority**: This enhances user experience by allowing them to view tasks in an order that makes sense for their current needs, making the application more flexible and efficient.

**Independent Test**: Can be fully tested by creating tasks with different attributes, then using sort parameters to verify that tasks are returned in the correct order, delivering the value of organized task presentation.

**Acceptance Scenarios**:

1. **Given** a user has tasks with different priorities, **When** they request /api/tasks?sort=priority, **Then** tasks are ordered with high priority first, then medium, then low
2. **Given** a user has tasks with different titles, **When** they request /api/tasks?sort=title, **Then** tasks are ordered alphabetically by title
3. **Given** a user has tasks in different categories, **When** they request /api/tasks?sort=category, **Then** tasks are grouped by category and ordered within each group
4. **Given** a user has tasks with different creation dates, **When** they request /api/tasks?sort=created, **Then** tasks are ordered by creation date (newest first)

---

### Edge Cases

- What happens when a user provides a search term that matches both title and description?
- How does the system handle very long search terms or special characters?
- What occurs when a user tries to filter by a category they don't have any tasks in?
- How does the system handle concurrent requests with different filters from the same user?
- What happens when the database query takes too long to execute?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST accept priority and category fields in POST /api/tasks requests
- **FR-002**: System MUST default priority to "medium" when not provided in create requests
- **FR-003**: System MUST allow null/empty category in create requests
- **FR-004**: System MUST accept priority and category fields in PUT /api/tasks/{id} requests
- **FR-005**: System MUST update priority and category when provided in update requests
- **FR-006**: System MUST preserve existing task data when updating only specific fields
- **FR-007**: System MUST support priority filtering via GET /api/tasks?priority={high|medium|low}
- **FR-008**: System MUST support category filtering via GET /api/tasks?category={category}
- **FR-009**: System MUST support status filtering via GET /api/tasks?status={all|pending|completed}
- **FR-010**: System MUST support text search in title and description via GET /api/tasks?search={term}
- **FR-011**: System MUST support sorting by creation date via GET /api/tasks?sort=created
- **FR-012**: System MUST support sorting by title via GET /api/tasks?sort=title
- **FR-013**: System MUST support sorting by priority (high > medium > low) via GET /api/tasks?sort=priority
- **FR-014**: System MUST support sorting by category via GET /api/tasks?sort=category
- **FR-015**: System MUST validate priority values to ensure they are one of: high, medium, low
- **FR-016**: System MUST validate category values to ensure they are max 50 characters
- **FR-017**: System MUST validate sort parameter values to ensure they are one of: created, title, priority, category
- **FR-018**: System MUST validate search parameter values for security (prevent injection)
- **FR-019**: System MUST return appropriate HTTP status codes (200, 401, 403, 404, 422)
- **FR-020**: System MUST maintain backward compatibility with existing API requests
- **FR-021**: System MUST enforce user isolation (users can only access their own tasks)
- **FR-022**: System MUST require valid JWT authentication for all endpoints
- **FR-023**: System MUST combine multiple filters when provided together (AND logic)
- **FR-024**: System MUST return tasks with all required fields (id, user_id, title, description, completed, priority, category, created_at, updated_at)
- **FR-025**: System MUST handle case-insensitive text search in task titles and descriptions

### Key Entities

- **Task Creation Request**: Represents the data needed to create a new task (title, optional description, optional priority, optional category) with validation constraints
- **Task Update Request**: Represents the data needed to update an existing task (optional fields for title, description, priority, category, completion status) with validation constraints
- **Task Filter Criteria**: Represents the parameters (status, priority, category) used to narrow down task listings
- **Task Search Query**: Represents the text-based search term that matches against task titles and descriptions
- **Task Sort Criteria**: Represents the parameters (created, title, priority, category) used to order task listings
- **User Authentication Token**: Represents the JWT token that identifies the authenticated user and provides their user ID for task isolation

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create tasks with priority and category in under 300ms with 99.9% success rate
- **SC-002**: Users can update task priority and category in under 300ms with 99.9% success rate
- **SC-003**: Task filtering operations return results in under 500ms for datasets up to 10,000 tasks
- **SC-004**: Task search operations return results in under 1 second for datasets up to 10,000 tasks
- **SC-005**: Task sorting operations return results in under 500ms for datasets up to 10,000 tasks
- **SC-006**: All filter combinations work correctly (priority + status + category) with 100% accuracy
- **SC-007**: Text search finds matches in both title and description fields with 99% accuracy
- **SC-008**: Priority sorting correctly orders tasks (high > medium > low) 100% of the time
- **SC-009**: Category sorting groups tasks by category with 100% accuracy
- **SC-010**: Invalid parameter validation returns 422 errors with helpful messages 100% of the time
- **SC-011**: User isolation is maintained with 100% accuracy (users only see their own tasks)
- **SC-012**: Backward compatibility is preserved with 100% success rate (old requests still work)
- **SC-013**: API handles 1000 concurrent authenticated users without performance degradation
- **SC-014**: Authentication requirements are enforced with 100% accuracy
- **SC-015**: The system properly handles edge cases like special characters in search terms