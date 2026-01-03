# Feature Specification: Database Connection & Task Model

**Feature Branch**: `6-db-connection-task-model`
**Created**: 2025-01-07
**Status**: Draft
**Input**: User description: "# Task 2: Database Connection & Task Model Specification + Implementation # Phase II Backend – Connect to Neon PostgreSQL + Define Persistent Task Model You are an expert FastAPI + SQLModel engineer. Current Status: - Task 1 complete: Basic FastAPI server running with main.py, db.py, models.py, dependencies.py, routes/tasks.py, .env - CORS and health endpoints working Goal for Task 2: Fully set up Neon Serverless PostgreSQL connection and define the persistent Task model so that data survives restarts and supports multi-user isolation. Requirements: 1. Database Connection (in db.py) - Import create_engine from sqlmodel - Load DATABASE_URL from .env using python-dotenv (load_dotenv()) - Create engine: engine = create_engine( os.getenv("DATABASE_URL"), echo=True, # for development visibility future=True ) - Create get_session dependency: from sqlmodel import Session def get_session(): with Session(engine) as session: yield session - Make get_session a FastAPI dependency (Depends(get_session)) 2. Task Model (in models.py) - Import necessary modules: from sqlmodel import SQLModel, Field from typing import Optional from datetime import datetime - Define the Task model exactly like this: class Task(SQLModel, table=True): """Persistent Task model linked to Better Auth user""" id: Optional[int] = Field(default=None, primary_key=True) user_id: str = Field( foreign_key="user.id", index=True, description="UUID string from Better Auth user table" ) title: str = Field(max_length=200, min_length=1) description: Optional[str] = Field(default=None, max_length=1000) completed: bool = Field(default=False) created_at: datetime = Field(default_factory=datetime.utcnow) updated_at: datetime = Field( default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow} ) 3. Table Creation (in main.py) - Import models (import models or from models import Task) so metadata registers - Add startup event: @app.on_event("startup") def on_startup(): SQLModel.metadata.create_all(engine) - Note: Better Auth will automatically create the "user" table when first signup happens via frontend 4. Environment - .env must contain: DATABASE_URL=postgresql+psycopg2://... (your Neon connection string with sslmode=require) BETTER_AUTH_SECRET=your_same_strong_secret_as_frontend Expected Outcome After This Task: - Backend starts without error - On first request (after frontend signup), tables "user" and "task" appear in Neon dashboard - Ready for CRUD operations in next tasks - All future tasks will be persistent and linked to authenticated users Refer to: @specs/database/schema.md @backend/CLAUDE.md Now implement Task 2 exactly as specified above. Ensure clean, readable code with proper imports and type hints. After implementation, the backend should be ready for JWT authentication and task routes."
**Constitution Compliance**: All features must adhere to project constitution principles

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Persistent Task Storage (Priority: P1)

A user wants their tasks to persist across application restarts and be available when they return to the application. The system stores tasks in a Neon PostgreSQL database so they survive server restarts.

**Why this priority**: Without persistent storage, users lose all their tasks when the application restarts, making the application essentially unusable for actual task management.

**Independent Test**: Can be fully tested by creating tasks, restarting the server, and verifying that tasks still exist, delivering the core value of persistent task management.

**Acceptance Scenarios**:

1. **Given** a user has created tasks, **When** the backend server is restarted, **Then** the tasks still exist when the server comes back online
2. **Given** the application is connected to Neon PostgreSQL, **When** a new task is created, **Then** it is stored in the database and retrievable later
3. **Given** a user has tasks in the database, **When** they access the application after a server restart, **Then** they can see their previously created tasks

---

### User Story 2 - Multi-User Data Isolation (Priority: P1)

Multiple users need to use the application simultaneously without seeing each other's tasks. The system ensures that each user only sees tasks associated with their account through proper linking to Better Auth user IDs.

**Why this priority**: Without proper user isolation, users would see and potentially modify each other's tasks, which is a critical security and privacy violation.

**Independent Test**: Can be fully tested by creating tasks with multiple user accounts and verifying that each user only sees their own tasks, delivering the core value of secure multi-user functionality.

**Acceptance Scenarios**:

1. **Given** User A has created tasks, **When** User B accesses the system, **Then** User B only sees their own tasks, not User A's tasks
2. **Given** two users are using the system simultaneously, **When** they both create tasks, **Then** they only see their respective tasks and not each other's
3. **Given** a user is authenticated, **When** they perform task operations, **Then** only tasks belonging to that user are affected

---

### User Story 3 - Database Connection Reliability (Priority: P2)

The application needs to maintain a stable connection to the Neon PostgreSQL database to ensure consistent availability of task data. The system establishes and maintains the database connection properly.

**Why this priority**: Without a reliable database connection, users may experience intermittent failures when accessing or modifying their tasks, leading to a poor user experience.

**Independent Test**: Can be fully tested by establishing a connection to Neon PostgreSQL and performing multiple operations without disconnection, delivering the value of reliable task management.

**Acceptance Scenarios**:

1. **Given** the application starts up, **When** it initializes, **Then** it successfully connects to the Neon PostgreSQL database
2. **Given** the application is running, **When** multiple database operations occur, **Then** the connection remains stable without interruption
3. **Given** there are temporary network issues, **When** the application experiences them, **Then** it recovers and maintains data integrity

---

### Edge Cases

- What happens when the database connection fails during a task operation?
- How does the system handle database connection timeouts?
- What occurs when the Neon PostgreSQL service is temporarily unavailable?
- How does the system handle very large task descriptions near the 1000 character limit?
- What happens when a user tries to access a task that was deleted by another process?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST establish a connection to Neon PostgreSQL using the DATABASE_URL from environment variables
- **FR-002**: System MUST load database credentials from .env file using python-dotenv
- **FR-003**: System MUST create a SQLModel engine with appropriate settings (echo=True for dev, future=True)
- **FR-004**: System MUST provide a get_session dependency for FastAPI to handle database sessions
- **FR-005**: System MUST define a Task model with fields: id, user_id (foreign key to Better Auth user), title, description, completed, created_at, updated_at
- **FR-006**: System MUST enforce that title is between 1-200 characters
- **FR-007**: System MUST allow description to be optional with max 1000 characters
- **FR-008**: System MUST automatically set created_at and updated_at timestamps
- **FR-009**: System MUST automatically create database tables on application startup
- **FR-010**: System MUST link tasks to Better Auth users via user_id foreign key
- **FR-011**: System MUST ensure users can only access tasks associated with their user_id
- **FR-012**: System MUST handle database connection errors gracefully
- **FR-013**: System MUST use proper indexing on user_id for efficient queries
- **FR-014**: System MUST update the updated_at field whenever a task is modified
- **FR-015**: System MUST be compatible with Better Auth's automatic user table creation

### Key Entities

- **Task**: Represents a user's todo item with ID, user association, title, description, completion status, and timestamps
- **User**: Represents an authenticated user managed by Better Auth with UUID identifier (referenced via foreign key)
- **Database Session**: Represents a connection to the Neon PostgreSQL database for executing queries

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Tasks persist across application restarts with 100% reliability
- **SC-002**: Database connection establishes successfully on 99.9% of application startups
- **SC-003**: Users can only access their own tasks with 100% enforcement rate
- **SC-004**: Database operations complete successfully 99.5% of the time under normal load
- **SC-005**: Task creation, reading, updating, and deletion operations complete in under 200ms
- **SC-006**: Application handles 1000 concurrent database operations without connection errors
- **SC-007**: Database tables are created automatically on first startup with 100% success rate
- **SC-008**: Task title and description validation prevents entries outside specified length constraints
- **SC-009**: Multi-user isolation is maintained during simultaneous usage by 100 different users
- **SC-010**: System recovers from temporary database connection interruptions within 30 seconds