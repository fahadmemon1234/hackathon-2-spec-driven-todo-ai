# Data Model: Task Routes with Advanced Features

## Task Entity (Extended)
- **Fields**:
  - id: int (primary key, autoincrement)
  - user_id: str (UUID, foreign key to users.id from Better Auth)
  - title: str (not null, 1-200 characters)
  - description: str | None (optional, max 1000 characters)
  - completed: bool (default: false)
  - priority: str (optional, values: "high", "medium", "low", default: "medium")
  - category: str | None (optional, max 50 characters, e.g., "work", "personal", "health")
  - created_at: datetime (auto-generated on creation)
  - updated_at: datetime (auto-generated, updates on modification)
- **Validation**:
  - Title is required and must be between 1-200 characters
  - Description, if provided, must be under 1000 characters
  - Priority, if provided, must be one of "high", "medium", "low"
  - Category, if provided, must be under 50 characters
  - user_id must be a valid UUID format from JWT token
- **Relationships**: Many-to-one relationship with User entity (managed by Better Auth)
- **State Transitions**:
  - pending → completed (when user marks task as complete)
  - completed → pending (when user unmarks task as complete)
  - priority changes (high ↔ medium ↔ low)
  - category changes (any valid category name)

## User Entity (Managed by Better Auth)
- **Fields**:
  - id: str (UUID, primary key)
  - email: str (unique, managed by Better Auth)
  - created_at: datetime (managed by Better Auth)
- **Validation**:
  - Email must be valid email format
  - ID must be valid UUID format
- **Relationships**: One-to-many relationship with Task entity (one user to many tasks)

## Search Query Entity (Conceptual)
- **Fields**:
  - keyword: str (search term to match in title or description)
  - user_id: str (to limit search to authenticated user's tasks only)
- **Validation**:
  - Keyword must be non-empty
  - User ID must be valid UUID
- **Relationships**: Used to filter Task entities during search operations

## Filter Criteria Entity (Conceptual)
- **Fields**:
  - status: str | None (values: "all", "pending", "completed")
  - priority: str | None (values: "all", "high", "medium", "low")
  - category: str | None (category name or "all")
  - user_id: str (to limit filters to authenticated user's tasks only)
- **Validation**:
  - Values must be from allowed sets
  - User ID must be valid UUID
- **Relationships**: Used to filter Task entities during list operations

## Sort Criteria Entity (Conceptual)
- **Fields**:
  - field: str (values: "created", "title", "priority", "category")
  - direction: str (values: "asc", "desc", default: "desc" for created, "asc" for others)
- **Validation**:
  - Field must be from allowed set
  - Direction must be "asc" or "desc"
- **Relationships**: Used to order Task entities during list operations