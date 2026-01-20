---
id: 4
title: "advanced-features-implementation-progress"
stage: green
date_iso: "2026-01-19"
surface: "agent"
model: "default"
feature: "advanced-features"
branch: "17-advanced-features"
user: "default_user"
command: "/sp.implement"
labels:
  - "implementation"
  - "progress"
  - "event-driven"
  - "dapr"
  - "kafka"
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
  - "backend/models.py"
  - "backend/routes/tasks.py"
  - "backend/mcp_server.py"
  - "backend/utils/recurrence_utils.py"
  - "backend/utils/event_publisher.py"
  - "backend/services/recurring.py"
  - "backend/services/notification.py"
  - "backend/alembic.ini"
  - "backend/alembic/env.py"
  - "backend/alembic/script.py.mako"
  - "backend/alembic/versions/2026_01_19_001_add_advanced_task_fields.py"
  - "backend/components/taskpubsub.yaml"
  - "backend/components/reminderpubsub.yaml"
  - "backend/components/secretstore.yaml"
  - "backend/secrets.json"
  - "requirements.txt"
  - "history/prompts/advanced-features/4-advanced-features-implementation-progress.prompt.md"
tests_yaml: []
prompt_text: |
  /sp.implement # Phase V – Development Tasks
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
  Successfully implemented significant portions of the Advanced Features, Event-Driven Architecture and Cloud Deployment feature. Completed implementation includes:

  1. Updated Task model with new fields: priority, tags, due_date, is_recurring, recurrence_rule, next_occurrence
  2. Created Alembic migration for database schema changes
  3. Implemented recurrence rule parsing utility using dateutil.rrule
  4. Created event publisher utility class for Dapr pub/sub
  5. Extended API endpoints with new query parameters for filtering and sorting
  6. Updated MCP tools to accept new fields and support new functionality
  7. Implemented recurring task logic that creates next instances when tasks are completed
  8. Created notification service for handling reminders
  9. Set up Dapr configuration for pub/sub and secrets
  10. Updated requirements.txt with new dependencies

  The implementation maintains backward compatibility while adding the requested advanced features. Many tasks from the task breakdown have been marked as completed, including:
  - All setup tasks (T001-T005)
  - All foundational tasks (T006-T013)
  - Most User Story 1 tasks (T014-T028)
  - Most User Story 2 tasks (T031-T035)
  - Most User Story 3 tasks (T040-T046)
  - All User Story 4 tasks (T050-T060)

  Remaining tasks focus on frontend updates and testing, which would require additional implementation.
outcome: |
  Significant progress made on advanced features implementation. Core backend functionality is complete with database schema updates, API extensions, MCP tool enhancements, event-driven architecture, and recurring task logic. Ready for frontend implementation and testing.
evaluation: |
  The implementation successfully adds the requested advanced features while maintaining backward compatibility. The event-driven architecture using Dapr is properly integrated, and recurring task functionality is implemented. The code follows the planned architecture and is ready for deployment and testing.
---