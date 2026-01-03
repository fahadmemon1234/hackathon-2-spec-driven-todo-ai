# Data Model: Luxury Todo Frontend

## User Entity
- **Fields**:
  - id: string (unique identifier)
  - email: string (email address, required, unique)
  - password: string (hashed password, required)
  - createdAt: Date (account creation timestamp)
  - updatedAt: Date (last update timestamp)
- **Validation**:
  - Email must be valid email format
  - Password must meet minimum strength requirements
- **Relationships**: One-to-many with Task entity

## Task Entity
- **Fields**:
  - id: string (unique identifier)
  - title: string (task title, required, max 255 characters)
  - description: string (task description, optional, max 1000 characters)
  - completed: boolean (completion status, default: false)
  - createdAt: Date (task creation timestamp)
  - updatedAt: Date (last update timestamp)
  - userId: string (foreign key to User)
- **Validation**:
  - Title is required and cannot be empty
  - Description, if provided, must be under 1000 characters
- **State Transitions**:
  - pending → completed (when user marks task as complete)
  - completed → pending (when user unmarks task as complete)

## Authentication Session
- **Fields**:
  - token: string (JWT token)
  - userId: string (associated user)
  - expiresAt: Date (token expiration)
- **Validation**:
  - Token must be valid JWT
  - Session must not be expired