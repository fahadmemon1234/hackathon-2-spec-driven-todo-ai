# Quickstart Guide: Single Task Operations

## Prerequisites
- Python 3.13+
- pip package manager
- Backend project with JWT authentication and database connection already set up
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

3. **Test the individual task endpoints**
   With a valid JWT token from Better Auth:
   
   Get a specific task:
   ```bash
   curl -X GET http://localhost:8000/api/tasks/1 \
     -H "Authorization: Bearer YOUR_VALID_JWT_TOKEN"
   ```
   
   Update a task:
   ```bash
   curl -X PUT http://localhost:8000/api/tasks/1 \
     -H "Authorization: Bearer YOUR_VALID_JWT_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"title": "Updated Task Title", "description": "Updated description"}'
   ```
   
   Delete a task:
   ```bash
   curl -X DELETE http://localhost:8000/api/tasks/1 \
     -H "Authorization: Bearer YOUR_VALID_JWT_TOKEN"
   ```
   
   Toggle task completion:
   ```bash
   curl -X PATCH http://localhost:8000/api/tasks/1/complete \
     -H "Authorization: Bearer YOUR_VALID_JWT_TOKEN"
   ```

## API Integration
- The individual task endpoints are protected with JWT authentication
- All operations enforce user ownership (users can only access their own tasks)
- Proper error handling with appropriate status codes (401, 403, 404)
- Input validation for task updates (title: 1-200 chars, description: 0-1000 chars)

## Key Features
- Secure individual task retrieval with ownership verification
- Full task updates with validation
- Safe task deletion with ownership check
- Efficient completion status toggling
- Proper error responses for unauthorized access attempts
- Consistent response models across all endpoints