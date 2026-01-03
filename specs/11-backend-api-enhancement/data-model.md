# Data Model: Backend API Enhancement

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

## TaskCreate Request Entity
- **Fields**:
  - title: str (required, 1-200 characters)
  - description: str | None (optional, max 1000 characters)
  - priority: str | None (optional, values: "high", "medium", "low", default: "medium")
  - category: str | None (optional, max 50 characters)
- **Validation**:
  - Title is required and must be between 1-200 characters
  - Description, if provided, must be under 1000 characters
  - Priority, if provided, must be one of "high", "medium", "low"
  - Category, if provided, must be under 50 characters
- **Relationships**: Maps to Task entity for creation operations

## TaskUpdate Request Entity
- **Fields**:
  - title: str | None (optional, 1-200 characters if provided)
  - description: str | None (optional, max 1000 characters if provided)
  - priority: str | None (optional, values: "high", "medium", "low")
  - category: str | None (optional, max 50 characters)
  - completed: bool | None (optional)
- **Validation**:
  - If title is provided, it must be between 1-200 characters
  - If description is provided, it must be under 1000 characters
  - If priority is provided, it must be one of "high", "medium", "low"
  - If category is provided, it must be under 50 characters
- **Relationships**: Maps to Task entity for update operations

## User Entity (Managed by Better Auth)
- **Fields**:
  - id: str (UUID, primary key)
  - email: str (unique, managed by Better Auth)
  - created_at: datetime (managed by Better Auth)
- **Validation**:
  - Email must be valid email format
  - ID must be valid UUID format
- **Relationships**: One-to-many relationship with Task entity (one user to many tasks)

## Query Parameters Entity (Conceptual)
- **Fields**:
  - status: str | None (values: "all", "pending", "completed", default: "all")
  - priority: str | None (values: "all", "high", "medium", "low", default: "all")
  - category: str | None (category name or "all", default: "all")
  - search: str | None (keyword to search in title or description)
  - sort: str (values: "created", "title", "priority", "category", default: "created")
- **Validation**:
  - Values must be from allowed sets
  - Search term must be properly sanitized to prevent injection
- **Relationships**: Used to filter and sort Task entities during list operations