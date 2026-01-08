# Quickstart Guide: AI-Powered Chatbot for Task Management

**Feature**: 14-ai-chatbot-task-management
**Created**: 2026-01-06

## Overview
This guide provides step-by-step instructions to set up and run the AI-powered chatbot for task management.

## Prerequisites
- Python 3.13+
- Node.js 20+
- UV package manager
- Access to OpenAI API key
- Access to Neon database (or local PostgreSQL)

## Setup Instructions

### 1. Clone and Navigate to Project
```bash
git clone <your-repo-url>
cd todo-app-Phase-3
```

### 2. Set Up Backend Environment
```bash
# Create and activate virtual environment
uv venv
source .venv/Scripts/activate  # On Windows
# source .venv/bin/activate    # On Linux/Mac

# Install dependencies
uv pip install -r requirements.txt

# Install new dependencies for AI chatbot
pip install mcp[fastapi] openai-agents
```

### 3. Set Up Frontend Environment
```bash
cd frontend
npm install
npm install @openai/chatkit
```

### 4. Configure Environment Variables
Create or update your `.env` file with the following variables:

```env
# Backend
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=your_neon_database_url
SECRET_KEY=your_secret_key

# Frontend
NEXT_PUBLIC_OPENAI_API_KEY=your_openai_api_key
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your_domain_key  # Required for production after domain allowlist
```

### 5. Run Database Migrations
```bash
# From the project root
python -m backend.database.migrate
```

### 6. Start the Backend Server
```bash
# From the project root
uvicorn backend.main:app --reload
```

### 7. Start the Frontend Server
```bash
# From the frontend directory
cd frontend
npm run dev
```

## Using the Chatbot

1. Open your browser and navigate to `http://localhost:3000`
2. Log in with your credentials
3. Navigate to the `/chat` route
4. Start interacting with the AI assistant using natural language:
   - "Add a task to buy milk tomorrow"
   - "Show my pending tasks"
   - "Mark the groceries task as done"
   - "Delete task 5"

## Development Workflow

### Backend Development
- MCP server is implemented in `backend/mcp_server.py`
- Chat endpoint is in `backend/routes/chat.py`
- Data models are in `backend/models.py`

### Frontend Development
- Chat interface is in `frontend/app/chat/page.tsx`
- The OpenAI ChatKit component is integrated in the chat page

## Troubleshooting

### Common Issues

1. **MCP Server Not Responding**
   - Ensure the MCP router is properly mounted in `main.py`
   - Check that the endpoint is accessible at `/mcp`

2. **Authentication Issues**
   - Verify JWT tokens are properly configured
   - Ensure user_id in path matches the authenticated user

3. **OpenAI Agent Not Responding**
   - Check that the OpenAI API key is valid
   - Verify that MCP tools are properly connected

### Domain Allowlist (Production)
If deploying to production:
1. Deploy frontend first (Vercel/Netlify/etc.)
2. Go to: https://platform.openai.com/settings/organization/security/domain-allowlist
3. Add your production domain (e.g., mytodoapp.vercel.app)
4. Get domain key and set as NEXT_PUBLIC_OPENAI_DOMAIN_KEY env var
5. Localhost works without allowlist for development

## Next Steps
- Review the implementation plan in `plan.md`
- Check the data model in `data-model.md`
- Look at API contracts in the `contracts/` directory
- Examine research findings in `research.md`