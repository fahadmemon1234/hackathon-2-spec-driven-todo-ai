---
id: 1
title: "Luxury Todo Frontend Spec"
stage: spec
date: "2025-01-07"
surface: "agent"
model: "Qwen"
feature: "luxury-todo-frontend"
branch: "4-luxury-todo-frontend"
user: "user"
command: "/sp.specify"
labels: ["frontend", "authentication", "ui", "ux"]
links:
  spec: "./spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - "specs/4-luxury-todo-frontend/spec.md"
  - "specs/4-luxury-todo-frontend/checklists/requirements.md"
tests: []
---

# Luxury Todo Frontend Spec

## User Input

```
Professional Prompt for Claude Code to Build Luxury Todo Frontend You are an expert Next.js 16 (App Router) developer with TypeScript, Tailwind CSS, and modern UI/UX design skills. Project Context: This is Phase II of the Todo App project – a full-stack multi-user web application. We are now implementing ONLY the frontend in a monorepo structure. The backend (FastAPI) is not yet implemented, but the API endpoints are fully specified in @specs/api/rest-endpoints.md Key Requirements for this task: - Implement ALL 5 basic CRUD features in the web frontend: 1. Add new task (title + description) 2. View/list all tasks with status indicators 3. Update task details 4. Delete task 5. Mark task as complete/incomplete (toggle) - The UI must be PROFESSIONAL, MODERN, and LUXURIOUS in feel. - Use a dark-themed luxury design with the exact color palette: - Primary accent: #d90429 (deep red – use for buttons, highlights, active states) - Secondary accent: #f6d72d (gold/yellow – use for icons, borders, subtle highlights) - Background and main text: #252525 (very dark gray – base background) - Additional colors you may use sparingly: - Card backgrounds: #1e1e1e or #2a2a2a (slightly lighter than base) - Text: #ffffff (primary), #cccccc (secondary), #f6d72d for completed task accents - Success/completed: subtle green or keep gold #f6d72d - Borders: thin #f6d72d or #d904294d (low opacity) Design Guidelines for Luxury Feel: - Clean, minimalist layout with generous spacing - Elegant typography: Use system fonts or Inter/Google Fonts if added, with bold headings - Subtle shadows, rounded corners (md or lg), hover animations (scale, brightness) - Glassmorphism or subtle gradients using the theme colors - Smooth transitions and micro-interactions - Task cards should feel premium – like high-end app dashboard - Loading states and empty states should be beautifully designed - Responsive: Mobile-first, works perfectly on desktop and mobile Frontend Stack: - Next.js 16+ (App Router) - TypeScript - Tailwind CSS (must use utility classes, no custom CSS unless necessary) - Better Auth for authentication (JWT-based) - API client to call backend at http://localhost:8000/api/tasks (during dev) Authentication: - Implement full user authentication using Better Auth: - Signup page - Signin page - Protected routes – redirect to login if not authenticated - After login, user can access the main todo dashboard - Better Auth must be configured to use JWT tokens - All API requests must include the JWT in Authorization: Bearer header Project Structure (inside /frontend): - /app – App Router pages and layouts - /components – All reusable UI components (TaskCard, TaskForm, TaskList, Auth forms, etc.) - /lib/api.ts – Centralized API client that: - Gets JWT from Better Auth session - Attaches Authorization header automatically - Base URL: http://localhost:8000 - Handles errors (401 → logout/redirect) - /styles/globals.css – Tailwind imports Pages to Implement: 1. /app/page.tsx → Landing page (if not logged in → show login/signup, if logged in → redirect to /tasks) 2. /app/login/page.tsx → Login form 3. /app/signup/page.tsx → Signup form 4. /app/tasks/page.tsx → Main dashboard with task list, add form, filters 5. Optional: Modal or separate page for edit task Features in Detail: - Task List: - Show tasks in beautiful cards or list - Checkbox to toggle complete (with gold strike-through or highlight) - Edit button (opens modal/form) - Delete button (with confirmation) - Show created date, status badge - Add Task: - Floating action button (FAB) in red #d90429 with gold icon - Or inline form at top - Modal form for luxury feel - Empty state: Beautiful message with illustration or subtle animation - Error handling: Toast notifications (use react-hot-toast or similar, but keep lightweight) Refer to these specs before implementing: @specs/features/task-crud.md @specs/features/authentication.md @specs/api/rest-endpoints.md @specs/ui/components.md (if exists, else create based on this) @frontend/CLAUDE.md Additional Instructions: - Follow all guidelines in /frontend/CLAUDE.md - Use server components where possible, client components only for interactivity - All interactive parts ('use client') - Implement proper loading skeletons while fetching tasks - Make it fully functional assuming backend works (handle success/error responses) - Use optimistic updates where possible for better UX - Ensure the design feels expensive and premium – think high-end productivity app Task: Implement the complete authenticated frontend with luxury UI as described above. Start by setting up Better Auth with JWT plugin enabled. Then implement auth pages. Then implement the main tasks dashboard with all CRUD operations. Use the exact color theme specified. Make it beautiful, responsive, and professional.
```

## Response Summary

Created a comprehensive feature specification for the luxury todo frontend based on the user's requirements. The specification includes:

1. User scenarios and testing with prioritized user stories
2. Functional requirements covering authentication, task management, and UI elements
3. Key entities involved in the system
4. Success criteria with measurable outcomes

The specification follows the template structure and focuses on user value without implementation details. A quality checklist was also created to validate the specification meets all requirements.

## Outcome

The feature specification is complete and ready for the planning phase. It covers all the requirements mentioned in the user's description while maintaining focus on user value and business needs.