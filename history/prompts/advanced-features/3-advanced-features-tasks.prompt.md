---
id: 3
title: "advanced-features-tasks"
stage: tasks
date_iso: "2026-01-19"
surface: "agent"
model: "default"
feature: "advanced-features"
branch: "17-advanced-features"
user: "default_user"
command: "/sp.tasks"
labels:
  - "tasks"
  - "breakdown"
  - "planning"
  - "event-driven"
  - "dapr"
  - "kubernetes"
links:
  spec: "@specs/17-advanced-features/spec.md"
  plan: "@specs/17-advanced-features/plan.md"
  tasks: "@specs/17-advanced-features/tasks.md"
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "specs/17-advanced-features/tasks.md"
  - "history/prompts/advanced-features/3-advanced-features-tasks.prompt.md"
tests_yaml: []
prompt_text: |
  /sp.tasks # Phase V – Development Tasks
  Advanced Features, Event-Driven Architecture (Kafka + Dapr) & Cloud Deployment

  ## Guiding Principles
  - Only extend, never remove or replace existing functionality
    (REST API, Better Auth + JWT, /api/{user_id}/chat, existing MCP tools)
  - Work incrementally → commit after each major sub-phase
  - Test locally on Minikube before moving to cloud
  - Prefer Oracle Cloud Always Free (OKE) as cloud target
  - Use Dapr to abstract Pub/Sub and other integrations

  ## Execution Phases & Tasks

  ### Phase 1: Database Schema & Migration
  Goal: Add new task fields without breaking existing data

  1. Update SQLModel Task class
     - priority: Enum("low", "medium", "high", "urgent"), default="medium"
     - tags: list[str] → JSON column
     - due_date: Optional[datetime]
     - is_recurring: bool = False
     - recurrence_rule: Optional[str]
     - next_occurrence: Optional[datetime]

  2. Create Alembic migration
     - Add columns
     - Add indexes: priority, due_date, (user_id, due_date)

  3. Write migration test
     - Ensure existing tasks receive sensible defaults

  4. Apply migration locally and verify

  ### Phase 2: Extend REST API & MCP Tools
  Goal: Let clients & AI agent use new task properties

  1. Update request/response models (Pydantic)
     - Add new fields to CreateTask / UpdateTask schemas
     - Add new optional query parameters to list tasks endpoint

  2. Extend GET /api/{user_id}/tasks
     - Support filtering: priority, tags, q (search), due_after/due_before
     - Support sorting: priority, due_date, title, created_at (+ descending with -)

  3. Update MCP tools
     - add_task: accept priority, tags, due_date, is_recurring, recurrence_rule
     - update_task: allow updating new fields
     - list_tasks: pass through new filters/sorting

  4. Add basic validation for recurrence_rule (simple string check)

  ### Phase 3: Enhance Chatbot Intent Recognition
  Goal: Teach the AI to handle new task attributes naturally

  1. Update agent instructions / prompt
     - Recognise priority: "urgent", "high priority", "low priority"
     - Due date parsing: "by next Friday", "tomorrow evening", "in 3 days"
     - Recurring: "every week", "every Monday", "monthly on the 10th"
     - Tags: "tag it as work", "add personal tag"

  2. When due_date is set → calculate remind_at (e.g. due_date - 1 hour)
     - Store remind_at in reminder event

  3. When recurring task completed → set next_occurrence before publishing event

  ### Phase 4: Add Event Publishing (initial direct Kafka client)
  Goal: Make chat-api produce events

  1. Add kafka producer utility (kafka-python or aiokafka)
  2. After successful DB operations in MCP tools, publish:
     - to "task-events": create / update / complete / delete
     - to "reminders": when due_date is set or changed
  3. Implement simple event schemas (as defined in spec)

  ### Phase 5: Create New Microservices
  Goal: Handle event consumption

  1. recurring-task-service (new FastAPI or simple script)
     - Consume "task-events"
     - On "completed" → if is_recurring → calculate next task → create it

  2. notification-service (minimal)
     - Consume "reminders"
     - Log the reminder (for hackathon) or send dummy HTTP request

  3. (Optional – time permitting) audit-service
     - Consume "task-events"
     - Store minimal log entries in new DB table

  ### Phase 6: Introduce Dapr & Replace Direct Kafka Client
  Goal: Decouple services from Kafka details

  1. Configure Dapr locally (dapr init -k for Minikube)
  2. Create Dapr components YAML
     - pubsub (pointing to Kafka/Redpanda)
     - cron binding (for periodic reminder check)
     - secret store (for Kafka credentials, DB url)

  3. Refactor chat-api, recurring-task-service & notification-service
     - Replace kafka-python with Dapr HTTP/gRPC calls
     - Publish via Dapr pub/sub
     - Subscribe via /dapr/subscribe endpoint

  4. Use Dapr secrets for sensitive values

  ### Phase 7: Local Deployment on Minikube
  Goal: Validate full flow locally

  1. Extend existing Helm charts (frontend, chat-api)
  2. Add Helm chart / manifests for:
     - recurring-task-service
     - notification-service
     - Dapr components
     - Redpanda (single node) or Strimzi Kafka

  3. Deploy everything
     - minikube start
     - helm upgrade / kubectl apply
     - dapr init -k

  4. Test end-to-end scenarios
     - Create recurring task with due date via chat
     - Complete task → check next instance appears
     - Check notification-service logs reminder

  ### Phase 8: Cloud Deployment
  Goal: Run on real Kubernetes cluster

  1. Create cluster (recommended order)
     - Oracle OKE Always Free
     - Azure AKS ($200 credit)
     - Google GKE ($300 credit)

  2. Install Dapr on cluster
  3. Deploy Redpanda Cloud Serverless or Strimzi inside cluster
  4. Update Dapr pubsub component to point to chosen Kafka
  5. Deploy application using Helm / kubectl
  6. Verify connectivity & test basic flow

  ### Phase 9: CI/CD Pipeline
  Goal: Automate deployments

  1. Create .github/workflows/deploy.yml
     - Trigger: push to main
     - Steps:
       - Build & push Docker images (frontend, chat-api, recurring, notification)
       - Update Helm values / kubectl apply to cloud cluster
     - Use GitHub secrets for cluster credentials

  ### Phase 10: Monitoring & Documentation
  Goal: Finish polish

  1. Enable basic monitoring
     - Pod logs
     - Simple readiness/liveness probes
     - (optional) Prometheus + Grafana

  2. Update README
     - New architecture diagram (text or simple draw.io)
     - Setup instructions for Minikube and cloud
     - List of new features & how to use them

  3. (optional) Record short demo video

  ## Suggested Order of Claude Code Prompts
  1. Update database schema & create migration (Phase 1)
  2. Extend REST API & MCP tools (Phase 2)
  3. Update agent prompt for new features (Phase 3)
  4. Add event publishing (Phase 4)
  5. Implement recurring-task-service (Phase 5)
  6. Implement Dapr integration (Phase 6)
  7. Create Minikube deployment manifests (Phase 7)

  Start with Phase 1 when you're ready.
response_text: |
  Successfully created a comprehensive task breakdown for the Advanced Features, Event-Driven Architecture and Cloud Deployment feature. The tasks.md file includes:

  1. 8 phases of work organized by user story priority
  2. 84 specific, actionable tasks with proper IDs and labels
  3. Clear dependencies and execution order
  4. Parallel execution opportunities identified
  5. Independent test criteria for each user story
  6. MVP scope defined (US1 - Enhanced Task Management)
  7. Incremental delivery strategy outlined

  The tasks follow the required checklist format with proper IDs, story labels, and file paths where applicable. Each task is specific enough for an LLM to complete without additional context. The breakdown maintains backward compatibility while adding the requested advanced features.

  Tasks cover all aspects of the implementation:
  - Database schema updates
  - API extensions
  - Event-driven architecture
  - New microservices
  - Dapr integration
  - Cloud deployment
  - Documentation and polish
outcome: |
  Task breakdown completed with 84 specific, actionable tasks organized across 8 phases. Each task follows the required checklist format with proper IDs and story labels. Ready for implementation phase.
evaluation: |
  The task breakdown comprehensively covers all requirements from the feature specification and implementation plan. Tasks are organized by user story priority to enable independent implementation and testing. Each task is specific and actionable with proper formatting.
---