# Data Model: Single Task Operations

## Task Entity (Existing)
- **Fields**:
  - id: int (primary key, autoincrement)
  - user_id: str (UUID, foreign key to users.id from Better Auth)
  - title: str (not null, 1-200 characters)
  - description: str | None (optional, max 1000 characters)
  - completed: bool (default: false)
  - created_at: datetime (auto-generated on creation)
  - updated_at: datetime (auto-generated, updates on modification)
- **Validation**:
  - Title is required and must be between 1-200 characters
  - Description, if provided, must be under 1000 characters
  - user_id must be a valid UUID format from JWT token
- **Relationships**: One-to-one relationship with User entity (managed by Better Auth)
- **State Transitions**:
  - pending → completed (when user marks task as complete)
  - completed → pending (when user unmarks task as complete)

## TaskUpdate Request Entity
- **Fields**:
  - title: str | None (optional, 1-200 characters if provided)
  - description: str | None (optional, max 1000 characters if provided)
- **Validation**:
  - If title is provided, it must be between 1-200 characters
  - If description is provided, it must be under 1000 characters
  - Both fields are optional, allowing partial updates
- **Relationships**: Maps to Task entity for update operations

## Task ID Parameter Entity
- **Fields**:
  - id: int (path parameter for identifying specific task)
- **Validation**:
  - Must be a valid integer
  - Must correspond to an existing task
  - Task must belong to the authenticated user
- **Relationships**: Used by all single-task endpoints (GET, PUT, DELETE, PATCH) to identify specific tasks

## Query Parameters Entity (for GET /api/tasks)
- **Fields**:
  - status: str | None (values: "all", "pending", "completed", default: None)
  - sort: str | None (values: "created", "title", default: "created")
- **Validation**:
  - Status must be one of the allowed values
  - Sort must be one of the allowed values
- **Relationships**: Used by GET /api/tasks endpoint for filtering and sorting collections

## Ownership Verification Entity (Conceptual)
- **Fields**:
  - task_id: int (identifier of the task to check)
  - user_id: str (identifier of the authenticated user)
  - task_owner_id: str (identifier of the task's owner)
- **Validation**:
  - task_owner_id must equal user_id for access to be granted
  - If validation fails, return 403 Forbidden
- **Relationships**: Applied to all single-task operations to enforce user isolation