---
id: 1
title: "FastAPI Backend Auth Spec"
stage: spec
date: "2025-01-07"
surface: "agent"
model: "Qwen"
feature: "fastapi-backend-auth"
branch: "5-fastapi-backend-auth"
user: "user"
command: "/sp.specify"
labels: ["backend", "api", "authentication", "security"]
links:
  spec: "./spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - "specs/5-fastapi-backend-auth/spec.md"
  - "specs/5-fastapi-backend-auth/checklists/requirements.md"
tests: []
---

# FastAPI Backend Auth Spec

## User Input

```
# Phase II: FastAPI Backend Specification & Implementation Prompt (Latest Better Auth Compatible) # Frontend: Complete with Better Auth + Manual JWT Bearer Token in API Calls # Date: December 31, 2025 – Better Auth v1.4+ (JWT Plugin or CookieCache JWT Strategy Enabled) You are an expert FastAPI developer with expertise in secure JWT auth, SQLModel, Neon PostgreSQL, and integrating with Better Auth. Project Goal: Implement the /backend folder as a secure, persistent, multi-user Todo API that seamlessly connects with the existing Phase II frontend. - All 5 basic features (Add, View, Update, Delete, Mark Complete) now persistent and user-isolated - Authentication via JWT Bearer token sent by frontend in Authorization header Key Facts from Better Auth (v1.4+): - Frontend configured for stateless mode (JWT strategy via cookieCache or JWT plugin) - After login, frontend manually extracts JWT and sends in Authorization: Bearer <token> - JWT signed with BETTER_AUTH_SECRET using HS256 algorithm - Payload contains user data, including user.id (string UUID) – use this as user_id - Better Auth auto-creates "user" table in DB on first signup API Endpoints (User from JWT – no user_id in path): Base: /api - GET /api/tasks → List authenticated user's tasks (?status=all|pending|completed &sort=created|title) - POST /api/tasks → Create task {title: required, description: optional} - GET /api/tasks/{id} → Get task (ownership check) - PUT /api/tasks/{id} → Update task - DELETE /api/tasks/{id} → Delete task - PATCH /api/tasks/{id}/complete → Toggle completed Security: - Every request must have valid Authorization: Bearer <jwt_token> - Verify token with PyJWT: jwt.decode(token, BETTER_AUTH_SECRET, algorithms=["HS256"]) - Extract user_id = payload.get("user", {}).get("id") or payload.get("id") # Better Auth structure - All task operations filter/enforce task.user_id == extracted_user_id - 401 Unauthorized: missing/invalid/expired token - 403 Forbidden: task not owned by user - 404 Not Found: task doesn't exist Tech Stack: - FastAPI (async preferred) - SQLModel (models + ORM) - Neon Serverless PostgreSQL (DATABASE_URL env) - PyJWT for verification (pip install pyjwt[cryptography]) - python-dotenv Structure (/backend): - main.py → app, routers, CORS (allow http://localhost:3000) - db.py → engine, get_session() - models.py → Task model (user_id: str FK to "user.id") - dependencies.py → get_current_user_id() dependency (JWT verify → return str user_id) - routes/tasks.py → APIRouter with all endpoints - .env → DATABASE_URL & BETTER_AUTH_SECRET (EXACT SAME as frontend!) Task Model Details: class Task(SQLModel, table=True): id: Optional[int] = Field(default=None, primary_key=True) user_id: str = Field(foreign_key="user.id", index=True) title: str description: Optional[str] = None completed: bool = False created_at: datetime = Field(default_factory=datetime.utcnow) updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow}) Features: - Auto timestamps - Filtering & sorting on list - Input validation (Pydantic) - Ownership enforced on every operation - Health endpoint /health - OpenAPI /docs Refer Specs: @specs/features/task-crud.md @specs/features/authentication.md @specs/api/rest-endpoints.md (update paths to /api/tasks) @specs/database/schema.md @backend/CLAUDE.md Task: Implement the complete backend exactly as specified. 1. Setup project, DB connection, models (tables auto-create) 2. JWT verification dependency (HS256 + BETTER_AUTH_SECRET) 3. Full CRUD routes with strict user isolation 4. CORS + polish 5. Update README: env vars (same secret!), run command 6. Suggest spec updates for endpoint simplification Result: Phase 1 in-memory → Phase 2 persistent multi-user full-stack with luxury frontend! Secure, production-ready, and perfectly integrated.
```

## Response Summary

Created a comprehensive feature specification for the FastAPI backend implementation with Better Auth integration based on the user's requirements. The specification includes:

1. User scenarios and testing with prioritized user stories
2. Functional requirements covering authentication, task management, and security
3. Key entities involved in the system
4. Success criteria with measurable outcomes

The specification follows the template structure and focuses on user value without implementation details. A quality checklist was also created to validate the specification meets all requirements.

## Outcome

The feature specification is complete and ready for the planning phase. It covers all the requirements mentioned in the user's description while maintaining focus on user value and business needs.