# Quickstart Guide: Task Routes with Advanced Features

## Prerequisites
- Python 3.13+
- Node.js 18+ (for frontend)
- PostgreSQL database (Neon or local)
- Better Auth secret key (same as frontend)

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd todo-app-Phase-2
   ```

2. **Backend setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   Create a `.env` file in the backend directory:
   ```env
   DATABASE_URL=postgresql+psycopg2://username:password@host:port/database_name?sslmode=require
   BETTER_AUTH_SECRET=your-super-secret-jwt-secret-here
   BETTER_AUTH_URL=http://localhost:3000
   ```

4. **Run the backend server**
   ```bash
   uvicorn main:app --reload --port 8000
   ```

5. **Frontend setup**
   ```bash
   cd frontend  # from repository root
   npm install
   ```

6. **Run the frontend server**
   ```bash
   npm run dev
   ```

## API Integration
- The backend connects to PostgreSQL database using the DATABASE_URL
- Better Auth manages user authentication and provides JWT tokens
- Task endpoints support priority levels (high, medium, low) and categories
- Search, filter, and sort functionality available on GET /api/tasks
- All endpoints require valid JWT tokens in Authorization header
- Tasks are properly isolated by user_id from JWT payload

## Key Features
- Task creation with priority and category assignment
- Task listing with filtering by status, priority, and category
- Task search by keyword in title or description
- Task sorting by creation date, title, priority, or category
- Visual priority indicators (color-coded)
- Category tags for organization
- Proper user isolation (users can only access their own tasks)
- Optimistic updates for better UX
- Responsive design for mobile and desktop

## Testing the Features
1. Create tasks with different priorities and categories
2. Use the search functionality to find tasks by keyword
3. Filter tasks by status (all, pending, completed)
4. Filter tasks by priority (high, medium, low)
5. Sort tasks by different criteria (created, title, priority, category)
6. Verify that users can only access their own tasks