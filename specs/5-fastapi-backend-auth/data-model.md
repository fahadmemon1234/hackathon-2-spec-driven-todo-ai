# Data Model: FastAPI Backend with Better Auth Integration

## Task Entity
- **Fields**:
  - id: int (primary key, autoincrement)
  - user_id: str (UUID, foreign key to users.id from Better Auth)
  - title: str (not null, max length 200)
  - description: str | None (optional, max length 1000)
  - completed: bool (default: false)
  - created_at: datetime (auto-generated)
  - updated_at: datetime (auto-generated, updates on modification)
- **Validation**:
  - Title is required and must be between 1-200 characters
  - Description, if provided, must be under 1000 characters
  - user_id must be a valid UUID format
- **Relationships**: One-to-one relationship with User entity (managed by Better Auth)
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

## JWT Token Entity (Conceptual)
- **Fields**:
  - token: str (JWT token string)
  - user_id: str (extracted from token payload)
  - expires_at: datetime (extracted from token payload)
- **Validation**:
  - Token must be valid JWT format
  - Token must be signed with the shared BETTER_AUTH_SECRET
  - Token must not be expired
- **Relationships**: Maps to User entity for authentication purposes