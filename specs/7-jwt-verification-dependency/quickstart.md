# Quickstart Guide: JWT Verification Dependency

## Prerequisites
- Python 3.13+
- pip package manager
- Better Auth secret key (same as frontend)

## Setup Instructions

1. **Install required dependencies**
   ```bash
   pip install python-jose[cryptography] python-dotenv
   ```

2. **Configure environment variables**
   Add to your `.env` file:
   ```env
   BETTER_AUTH_SECRET=your-super-secret-jwt-key-here
   ```

3. **Import and use the JWT verification dependency**
   In your route handlers:
   ```python
   from dependencies import get_current_user_id
   
   @router.get("/protected-endpoint")
   def protected_route(current_user_id: str = Depends(get_current_user_id)):
       # This endpoint is protected by JWT verification
       return {"user_id": current_user_id, "message": "Access granted"}
   ```

## Integration with Existing Backend

The JWT verification dependency is designed to integrate seamlessly with the existing backend structure:

1. **In routes/tasks.py**, protect endpoints with the dependency:
   ```python
   from fastapi import Depends
   from dependencies import get_current_user_id
   
   @router.get("/tasks")
   def get_tasks(current_user_id: str = Depends(get_current_user_id)):
       # Only returns tasks belonging to current_user_id
       pass
   ```

2. **All protected endpoints** should use `Depends(get_current_user_id)` to ensure authentication

## Key Features

- Secure JWT verification using BETTER_AUTH_SECRET with HS256 algorithm
- Flexible payload structure handling (supports both `user.id` and `id` fields)
- Proper error handling with appropriate HTTP status codes (401 for invalid tokens)
- Thread-safe for concurrent requests
- Environment variable configuration for security
- FastAPI dependency injection integration