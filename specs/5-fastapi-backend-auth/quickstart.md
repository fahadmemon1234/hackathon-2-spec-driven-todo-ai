# Quickstart Guide: FastAPI Backend with Better Auth Integration

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
   DATABASE_URL=postgresql+psycopg2://username:password@host:port/database_name
   BETTER_AUTH_SECRET=your-super-secret-jwt-secret-here
   ```

4. **Run the development server**
   ```bash
   uvicorn main:app --reload --port 8000
   ```

5. **Access the application**
   - API: [http://localhost:8000](http://localhost:8000)
   - API Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)
   - Health Check: [http://localhost:8000/health](http://localhost:8000/health)

## API Integration
- The backend connects to Neon PostgreSQL database using the DATABASE_URL
- JWT tokens from Better Auth are verified using the shared BETTER_AUTH_SECRET
- All endpoints require valid JWT tokens in Authorization header
- Tasks are properly isolated by user_id from JWT payload

## Key Features
- User authentication with JWT verification
- Create, read, update, delete tasks
- Mark tasks as complete/incomplete
- Filter and sort tasks
- Proper error handling with appropriate status codes
- Secure user isolation (users can only access their own tasks)
- CORS configured for frontend integration