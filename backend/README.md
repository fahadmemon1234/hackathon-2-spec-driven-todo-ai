# Todo Backend API

This is the backend API for the luxury todo application, built with FastAPI and integrated with Better Auth for authentication.

## Prerequisites

- Python 3.13+
- pip package manager
- Neon PostgreSQL account (or local PostgreSQL installation)
- Better Auth secret key (same as frontend)

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd todo-app-Phase-2/backend
   ```

2. **Create virtual environment and install dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the backend directory:
   ```env
   DATABASE_URL=postgresql+psycopg2://username:password@host:port/database_name?sslmode=require
   BETTER_AUTH_SECRET=your-super-secret-jwt-secret-here
   ```

4. **Run the development server**
   ```bash
   uvicorn main:app --reload --port 8000
   ```

## Environment Variables

- `DATABASE_URL`: PostgreSQL database connection string with sslmode=require
- `BETTER_AUTH_SECRET`: JWT secret key (must be the same as the frontend)

## API Endpoints

- `GET /`: Root endpoint
- `GET /health`: Health check endpoint
- `GET /docs`: API documentation
- `POST /api/tasks`: Create a new task
- `GET /api/tasks`: Get all tasks for authenticated user
- `GET /api/tasks/{id}`: Get a specific task
- `PUT /api/tasks/{id}`: Update a task
- `DELETE /api/tasks/{id}`: Delete a task
- `PATCH /api/tasks/{id}/complete`: Toggle task completion status

## Key Features

- User authentication with JWT verification using Better Auth
- Create, read, update, delete tasks
- Mark tasks as complete/incomplete
- Filter and sort tasks
- Proper error handling with appropriate status codes
- Secure user isolation (users can only access their own tasks)
- CORS configured for frontend integration
- Automatic timestamps for created_at and updated_at fields