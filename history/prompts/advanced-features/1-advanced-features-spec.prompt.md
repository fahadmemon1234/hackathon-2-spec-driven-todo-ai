---
id: 1
title: "advanced-features-spec"
stage: spec
date_iso: "2026-01-19"
surface: "agent"
model: "default"
feature: "advanced-features"
branch: "17-advanced-features"
user: "default_user"
command: "/sp.specify"
labels:
  - "specification"
  - "feature"
  - "advanced-features"
  - "event-driven"
links:
  spec: "@specs/17-advanced-features/spec.md"
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "specs/17-advanced-features/spec.md"
  - "specs/17-advanced-features/checklists/requirements.md"
  - "history/prompts/advanced-features/1-advanced-features-spec.prompt.md"
tests_yaml: []
prompt_text: |
  # Phase V: Advanced Features, Event-Driven Architecture and Cloud Deployment

  ## Objective
  Extend the Todo AI Chatbot with intermediate and advanced task management features, introduce an event-driven architecture using Kafka (or compatible Pub/Sub) and Dapr, and deploy the application first locally on Minikube and then to a production-grade Kubernetes cluster (preferably Oracle OKE Always Free, alternatively Azure AKS or Google GKE).

  ## Core Constraints
  - Do NOT remove or replace existing REST API endpoints under /api/{user_id}/tasks
  - Do NOT remove or replace Better Auth + JWT authentication
  - Do NOT remove or replace the /api/{user_id}/chat endpoint
  - Do NOT remove or replace existing MCP tools (add_task, list_tasks, complete_task, delete_task, update_task)
  - Only **add** new fields, endpoints, tools, services and event flows
  - Continue using Neon Serverless PostgreSQL as the main database
  - Use Dapr to abstract Pub/Sub, Bindings, Secrets and Service Invocation

  ## Part A – Feature Requirements

  ### A.1 Intermediate Features (add to Task entity)
  | Field | Type | Description | Required | Default |
  |----------------|-----------------------|--------------------------------------------------|----------|-------------|
  | priority | Enum | low, medium, high, urgent | no | medium |
  | tags | array of strings | short labels (e.g. ["work", "urgent"]) | no | empty |
  | due_date | datetime | when the task should be finished | no | null |

  Additional API capabilities:
  - GET /api/{user_id}/tasks supports query parameters:
    - ?priority=high,urgent
    - ?tags=work,personal
    - ?q=keyword (search in title + description)
    - ?sort=priority,-due_date,title,created_at
    - ?due_after=YYYY-MM-DD & ?due_before=YYYY-MM-DD

  ### A.2 Advanced Features
  | Field | Type | Description | Required | Default |
  |--------------------|----------|-------------------------------------------------------|----------|---------|
  | is_recurring | boolean | whether the task repeats | no | false |
  | recurrence_rule | string | simple pattern: "DAILY", "WEEKLY:Mon,Wed", "MONTHLY:15", "YEARLY" | no | null |
  | next_occurrence | datetime | date/time of the next instance (managed by system) | no | null |

  Behavior:
  - When a recurring task is marked complete → system creates the next instance according to recurrence_rule
  - When a task has a due_date → system schedules a reminder (e.g. 1 hour before due_date)

  ### A.3 Natural Language Support in Chatbot
  The AI agent should understand and handle (among others):
  - "Add a high-priority task to prepare presentation by next Wednesday"
  - "List all urgent tasks tagged work"
  - "Remind me to pay rent every month"
  - "Make this task repeat every Monday morning"

  ## Part B – Event-Driven Architecture

  ### B.1 Kafka Topics
  | Topic | Producer | Main Consumers | Purpose |
  |---------------|-----------------------------------|---------------------------------------|------------------------------------------|
  | task-events | Chat API (after task CRUD) | Recurring Task Service, Audit Service | created, updated, completed, deleted |
  | reminders | Chat API (when due_date set) | Notification Service | trigger notifications |
  | task-updates | Chat API (after any change) | (optional) WebSocket Service | real-time client synchronization |

  ### B.2 Event Schemas (JSON)

  **task-events**
  ```json
  {
    "event_type": "created" | "updated" | "completed" | "deleted",
    "task_id": number,
    "user_id": string,
    "task_data": { ... complete task object ... },
    "timestamp": "2026-01-18T22:15:00Z"
  }
  ```

  **reminders**
  ```json
  {
    "task_id": number,
    "user_id": string,
    "title": string,
    "due_at": "2026-01-20T18:00:00Z",
    "remind_at": "2026-01-20T17:00:00Z",
    "timestamp": "2026-01-18T22:15:00Z"
  }
  ```

  Part C – Dapr Usage
  Use the following Dapr building blocks:

  | Building Block | Purpose in this project |
  |----------------|-------------------------|
  | Pub/Sub | Publish & consume events (instead of kafka-python) |
  | Bindings (Cron) | Periodically check for due reminders |
  | Secrets | Store Kafka/Redpanda credentials, Neon DB URL |
  | Service Invocation | Internal service-to-service calls (optional) |
  | State (optional) | Short-lived data if needed |

  Part D – Deployment Targets
  D.1 Local (Minikube)
  - Deploy existing frontend & chat-api services (from Phase IV Helm charts)
  - Deploy Dapr on Minikube
  - Deploy Kafka/Redpanda inside cluster (recommended: Redpanda single-container)
  - Deploy new services: recurring-task-service, notification-service
  - Use Dapr Pub/Sub component pointing to Kafka/Redpanda

  D.2 Cloud (preferred order)
  - Oracle Cloud OKE – Always Free tier (4 OCPUs, 24 GB RAM)
  - Azure AKS – $200 free credit
  - Google GKE – $300 free credit

  D.3 Kafka / PubSub Options
  - Preferred for cloud: Redpanda Cloud Serverless (free tier)
  - Alternative: Strimzi Kafka operator inside the Kubernetes cluster
  - Fallback: Any other Dapr-supported Pub/Sub component

  Part E – Additional Requirements
  - Set up GitHub Actions CI/CD pipeline to build Docker images and deploy to cluster
  - Add basic monitoring & logging (at minimum: pod logs + simple health checks)
  - Update README with new architecture overview and setup instructions

  Part F – Acceptance Criteria
  - Task table contains new columns: priority, tags, due_date, is_recurring, recurrence_rule, next_occurrence
  - REST API supports new query parameters for filtering, sorting and search
  - MCP tools add_task and update_task accept new fields
  - Creating a task with due_date publishes a reminder event
  - Completing a recurring task triggers creation of the next instance
  - Notification service receives reminder events and logs them
  - All services use Dapr sidecars for Pub/Sub and Secrets
  - Application runs successfully on Minikube
  - Application is deployed to a cloud Kubernetes cluster
  - GitHub Actions pipeline can deploy changes

  Related Specifications
  - Update: @specs/database/schema.md
  - Update: @specs/api/rest-endpoints.md
  - Update: @specs/api/mcp-tools.md
  - New: specs/features/recurring-tasks.md
  - New: specs/features/reminders.md
  - New: specs/infrastructure/dapr.md
  - New: specs/infrastructure/pubsub.md

  text**Next steps you can take:**
  1. Save the content above as `specs/features/phase5-advanced-features.md`
  2. Create the plan yourself or ask me to make one based on this spec
  3. Give Claude Code a prompt like: Read @specs/features/phase5-advanced-features.md Create a step-by-step implementation plan Start by updating the database schema
response_text: |
  Created feature specification for advanced features, event-driven architecture, and cloud deployment. The specification includes:
  
  1. Enhanced task management with priority, tags, and due dates
  2. Recurring tasks functionality with automatic next instance creation
  3. Task reminder system that triggers notifications
  4. Event-driven architecture using Kafka/Dapr for service communication
  5. Cloud deployment capabilities for Kubernetes
  
  The specification follows the template structure with user scenarios, functional requirements, and success criteria. A checklist was also created to validate the specification quality. The feature branch '17-advanced-features' was created for this work.
outcome: |
  Successfully created feature specification document at specs/17-advanced-features/spec.md with comprehensive requirements for advanced task management features, event-driven architecture, and cloud deployment. Created validation checklist and feature branch.
evaluation: |
  The specification is complete and ready for the planning phase. All requirements from the original description have been captured in a structured format that focuses on user value rather than implementation details.
---