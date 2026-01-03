# Quickstart Guide: Task Routes Implementation

## Prerequisites
- Python 3.13+
- pip package manager
- Backend project initialized with FastAPI, SQLModel, and JWT authentication
- Better Auth secret key configured (same as frontend)

## Setup Instructions

1. **Verify backend is running**
   ```bash
   cd backend
   uvicorn main:app --reload --port 8000
   ```

2. **Ensure environment variables are set**
   Verify your `.env` file contains:
   ```env
   DATABASE_URL=postgresql+psycopg2://username:password@host:port/database_name
   BETTER_AUTH_SECRET=your-super-secret-jwt-secret-here
   ```

3. **Test the endpoints**
   With a valid JWT token from Better Auth:
   
   Create a task:
   ```bash
   curl -X POST http://localhost:8000/api/tasks \
     -H "Authorization: Bearer YOUR_VALID_JWT_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"title": "Test Task", "description": "This is a test task"}'
   ```
   
   List tasks:
   ```bash
   curl -X GET "http://localhost:8000/api/tasks?status=all&sort=created" \
     -H "Authorization: Bearer YOUR_VALID_JWT_TOKEN"
   ```

## API Integration
- The task endpoints are protected with JWT authentication
- All operations are filtered by the authenticated user's ID
- Tasks are properly isolated between different users
- Filtering and sorting options are available on the GET endpoint

## Key Features
- Secure task creation with user isolation
- Task listing with filtering (all/pending/completed)
- Task sorting (by creation date or title)
- Proper error handling with appropriate status codes
- Input validation for task titles and descriptions
- Automatic timestamp management