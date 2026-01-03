# Data Model: Database Connection & Task Model

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
  - Title must be between 1-200 characters
  - Description, if provided, must be under 1000 characters
  - user_id must be a valid UUID format from Better Auth
- **Relationships**: Many-to-one relationship with User entity (managed by Better Auth)
- **State Transitions**:
  - pending → completed (when user marks task as complete)
  - completed → pending (when user unmarks task as complete)

## User Entity (Managed by Better Auth)
- **Fields**:
  - id: str (UUID, primary key)
  - email: str (unique, managed by Better Auth)
  - created_at: datetime (managed by Better Auth)
- **Validation**:
  - Email must be valid email format
  - ID must be valid UUID format
- **Relationships**: One-to-many relationship with Task entity (one user to many tasks)

## Database Session Entity
- **Fields**:
  - session: SQLModel Session object
  - connection: Active connection to Neon PostgreSQL
- **Validation**:
  - Connection must be valid and active
  - Session must be properly closed after use
- **Relationships**: Used by all database operations to interact with Task and User entities