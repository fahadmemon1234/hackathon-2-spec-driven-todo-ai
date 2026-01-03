# Data Model: Task Routes Implementation

## Task Entity
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

## TaskCreate Request Entity
- **Fields**:
  - title: str (required, 1-200 characters)
  - description: str | None (optional, max 1000 characters)
- **Validation**:
  - Title is required and must be between 1-200 characters
  - Description, if provided, must be under 1000 characters
- **Relationships**: Maps to Task entity for creation operations

## TaskList Response Entity
- **Fields**:
  - tasks: List[Task] (collection of Task entities)
- **Validation**:
  - Only includes tasks belonging to the authenticated user
  - Optionally filtered by status (all/pending/completed)
  - Optionally sorted by creation date or title
- **Relationships**: Collection of Task entities returned by GET /api/tasks endpoint

## Query Parameters Entity
- **Fields**:
  - status: str | None (values: "all", "pending", "completed", default: None)
  - sort: str | None (values: "created", "title", default: "created")
- **Validation**:
  - Status must be one of the allowed values
  - Sort must be one of the allowed values
- **Relationships**: Used by GET /api/tasks endpoint for filtering and sorting