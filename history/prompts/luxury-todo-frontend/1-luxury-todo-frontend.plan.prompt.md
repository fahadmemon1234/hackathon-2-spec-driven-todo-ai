---
id: 1
title: "Luxury Todo Frontend Plan"
stage: plan
date: "2025-01-07"
surface: "agent"
model: "Qwen"
feature: "luxury-todo-frontend"
branch: "3-luxury-todo-frontend"
user: "user"
command: "/sp.plan"
labels: ["frontend", "authentication", "ui", "ux", "planning"]
links:
  spec: "../spec.md"
  plan: "./plan.md"
  research: "./research.md"
  data-model: "./data-model.md"
  quickstart: "./quickstart.md"
  ticket: null
  adr: null
  pr: null
files:
  - "specs/3-luxury-todo-frontend/plan.md"
  - "specs/3-luxury-todo-frontend/research.md"
  - "specs/3-luxury-todo-frontend/data-model.md"
  - "specs/3-luxury-todo-frontend/quickstart.md"
  - "specs/3-luxury-todo-frontend/contracts/tasks-api.yaml"
tests: []
---

# Luxury Todo Frontend Plan

## User Input

```
# Phase II: Frontend Only Implementation Plan (Luxury Todo Web App)
# Updated: December 30, 2025 – Better Auth v1.4.9 (latest & stable)
# Goal: Complete all 5 basic features + Authentication + Premium UI in /frontend folder
# Use this plan sequentially with Claude Code

Total Tasks: 7 (Ek baar mein ek task implement karo)

Task 1: Project Setup & Better Auth with JWT
Prompt to paste in Claude Code:
"Set up latest Better Auth (v1.4.9) in /frontend with JWT stateless session:
- Install command: npm install better-auth@latest
- Create /lib/auth.ts with email/password config + stateless JWT strategy
- Add BETTER_AUTH_SECRET and BETTER_AUTH_URL in .env.local
- Set up auth routes (/api/auth/*)
- Protect /tasks route with middleware or session check
- Add Inter font from next/font/google in root layout.tsx
- Follow latest Better Auth docs for Next.js App Router"

Task 2: Authentication Pages (Login + Signup + Landing)
Prompt:
"Implement luxury auth pages with theme #d90429 #f6d72d #252525:
- /app/page.tsx: Landing page (if logged in redirect to /tasks, else show login/signup buttons)
- /app/login/page.tsx: Beautiful centered login form (glassmorphism, gold button)
- /app/signup/page.tsx: Same style signup form
Use Better Auth signIn/signUp functions, elegant inputs, subtle animations"

Task 3: API Client with Mock Data & JWT Auto-Attach
Prompt:
"Create /lib/api.ts API client:
- Get JWT from Better Auth session automatically
- Add Authorization: Bearer <token> header to every request
- Base URL: http://localhost:8000
- Functions: getTasks(), createTask(data), getTask(id), updateTask(id, data), deleteTask(id), toggleComplete(id)
- For now, MOCK all responses with fake data (use array of 5-10 sample tasks)
- Include optimistic updates and basic error handling"

Task 4: Main Dashboard Layout & Add Task Feature
Prompt:
"Build protected /app/tasks/page.tsx dashboard:
- Header: User email + logout button (gold accent)
- Floating Action Button (FAB) bottom-right: #d90429 circle with gold + icon
- Opens TaskFormModal for adding new task (title required, description optional)
- Use glassmorphism cards, luxury spacing, responsive layout"

Task 5: Task List View + Mark Complete
Prompt:
"Implement task listing in dashboard:
- Fetch tasks using api.getTasks() (mocked)
- Display in responsive grid (mobile 1 col, desktop 2-3)
- TaskCard component: title, description (truncate), created date, status badge, checkbox to toggle complete (gold strike-through)
- Filters at top: All | Pending | Completed (gold underline active)
- Empty state: Elegant message 'No tasks yet, add your first!' with icon
- Loading skeleton while fetching"

Task 6: Update & Delete Tasks
Prompt:
"Add edit & delete functionality:
- Edit button on TaskCard → opens TaskFormModal pre-filled
- Delete button → opens confirmation modal (Are you sure?)
- Use api.updateTask() and api.deleteTask() with optimistic updates
- Show success/error toasts (use sonner or custom lightweight toast)
- Refresh list after operations"

Task 7: Final Polish & Responsiveness
Prompt:
"Polish the entire frontend:
- Add smooth transitions, hover effects (scale + gold glow), micro-interactions
- Ensure 100% responsive (test mobile + desktop)
- Add loading states everywhere
- Make UI feel truly luxurious & premium
- Fix any bugs, improve typography with Inter font
- Update @specs/ui/components.md with any new UI decisions"

Quick Testing Checklist (After All Tasks):
- Signup → Login → See /tasks dashboard
- Add 3-4 tasks
- Mark some complete (see gold styling)
- Edit one task
- Delete one task
- Logout → Redirect to landing
- Check mobile view

Deliverables:
- All code in /frontend
- Working luxury UI with all 5 features
- README update: cd frontend && npm install && npm run dev

Start with Task 1 right now!
First run in terminal: cd frontend && npm install better-auth@latest
```

## Response Summary

Completed the implementation planning workflow for the luxury todo frontend:

1. Created the implementation plan (plan.md) with technical context, constitution check, and project structure
2. Resolved the "NEEDS CLARIFICATION" item about testing approach in research.md
3. Defined the data model for User, Task, and Authentication Session entities
4. Created a quickstart guide with setup instructions
5. Defined API contracts for authentication and task management endpoints
6. Created a basic agent context file

The plan follows the luxury design requirements with the specified color palette and includes all 5 required CRUD features plus authentication.

## Outcome

The implementation plan is complete and ready for the task breakdown phase. All necessary design artifacts have been created, including data models, API contracts, and setup instructions.