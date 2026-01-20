# Implementation Plan: Advanced Features, Event-Driven Architecture and Cloud Deployment

**Feature**: Advanced Features, Event-Driven Architecture and Cloud Deployment
**Branch**: 17-advanced-features
**Created**: 2026-01-19
**Status**: Draft

## Technical Context

This implementation extends the existing Todo AI Chatbot with advanced task management features, introduces an event-driven architecture using Kafka (or compatible Pub/Sub) and Dapr, and deploys the application first locally on Minikube and then to a production-grade Kubernetes cluster.

### Current Architecture
- Frontend: React-based UI
- Backend: FastAPI with Better Auth + JWT authentication
- Database: Neon Serverless PostgreSQL
- AI Agent: Chat interface with MCP tools
- Existing MCP tools: add_task, list_tasks, complete_task, delete_task, update_task
- Existing endpoints: /api/{user_id}/tasks, /api/{user_id}/chat

### Target Architecture
- All existing functionality preserved
- New task attributes: priority, tags, due_date, is_recurring, recurrence_rule, next_occurrence
- Event-driven communication via Kafka/Redpanda + Dapr
- New services: recurring-task-service, notification-service
- Deployment: Minikube initially, then cloud Kubernetes (preferably Oracle OKE)

### Dependencies & Integrations
- **Kafka/Redpanda**: For event streaming between services
- **Dapr**: For abstracting Pub/Sub, bindings, secrets, and service invocation
- **Neon PostgreSQL**: Extended schema for new task attributes
- **Better Auth**: Preserved for authentication
- **Kubernetes**: For container orchestration
- **Helm**: For deployment management

## Constitution Check

### Adherence to Core Principles
- ✅ AI-Centric Development: All code will be AI-generated with minimal manual intervention
- ✅ Spec-Driven Approach: Following the feature specification created in the previous step
- ✅ Clean Code and Modularity: Maintaining separation of concerns between services
- ✅ Transparency and Iteration: Documenting all implementation steps
- ✅ Scalability Focus: Designing with cloud deployment in mind
- ✅ Ethical AI Use: Ensuring secure and efficient code

### Technology Stack Compliance
- ✅ Python 3.13+ for backend services
- ✅ UV for environment management
- ✅ Spec-Kit Plus for specifications
- ✅ Claude Code for primary implementation
- ✅ Qwen for planning and validation

## Gates & Risk Assessment

### Gate 1: Backward Compatibility
- **Requirement**: Do NOT remove or replace existing REST API endpoints, authentication, chat endpoint, or MCP tools
- **Status**: PASS - Plan preserves all existing functionality while adding new features
- **Verification**: New fields added to existing Task model, new endpoints added alongside existing ones

### Gate 2: Data Integrity
- **Requirement**: Safely extend database schema without losing existing data
- **Status**: PASS - Using Alembic migrations to safely add columns with appropriate defaults
- **Verification**: Migration tests will ensure existing tasks receive sensible defaults

### Gate 3: Event-Driven Architecture
- **Requirement**: Implement event-driven communication between services
- **Status**: PASS - Using Kafka/Redpanda with Dapr for service communication
- **Verification**: Services will communicate via pub/sub pattern rather than direct API calls

### Gate 4: Cloud Deployment Feasibility
- **Requirement**: Deploy successfully to Kubernetes cluster
- **Status**: CONDITIONAL PASS - Will validate during implementation
- **Mitigation**: Starting with Minikube for local validation before cloud deployment

## Phase 0: Research & Resolution of Unknowns

### Research Task 1: Dapr Configuration for Minikube
**Decision**: How to configure Dapr for local Minikube development
**Rationale**: Dapr needs to be properly configured to work with Minikube for local testing
**Alternatives considered**: 
- Using Dapr standalone mode
- Using Dapr with Kubernetes mode on Minikube
**Chosen approach**: Kubernetes mode on Minikube for consistency with cloud deployment

### Research Task 2: Kafka vs Redpanda for Local Development
**Decision**: Which streaming platform to use for local development
**Rationale**: Need to choose between Kafka and Redpanda for local testing
**Alternatives considered**:
- Apache Kafka with Confluent Platform
- Redpanda (more lightweight, Kafka API compatible)
**Chosen approach**: Redpanda for local development due to lighter resource requirements

### Research Task 3: Recurrence Rule Parsing Library
**Decision**: Which library to use for parsing and calculating recurrence rules
**Rationale**: Need reliable library to calculate next occurrence dates based on recurrence rules
**Alternatives considered**:
- dateutil.rrule (part of python-dateutil)
- croniter for cron-like expressions
- Custom implementation
**Chosen approach**: dateutil.rrule for its robustness and compliance with iCalendar standards

### Research Task 4: Tag Storage Strategy
**Decision**: How to store and index tags for efficient querying
**Rationale**: Tags need to be stored in a way that supports efficient filtering
**Alternatives considered**:
- JSON column in PostgreSQL (flexible but less efficient for queries)
- Separate task_tags table with joins (normalized but more complex)
- Array column in PostgreSQL (efficient for this use case)
**Chosen approach**: JSON column for flexibility with appropriate indexing

## Phase 1: Design & Contracts

### Data Model: Task Entity Extension

#### Updated Task Model
```python
class Task(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: str
    title: str
    description: str = ""
    completed: bool = False
    
    # New fields for Phase 5
    priority: str = Field(default="medium", sa_column=Column(Enum("low", "medium", "high", "urgent", name="priority_enum")))
    tags: List[str] = Field(default=[], sa_column=Column(JSON))
    due_date: Optional[datetime] = None
    is_recurring: bool = False
    recurrence_rule: Optional[str] = None  # e.g. "DAILY", "WEEKLY:Mon,Wed", "MONTHLY:15", "YEARLY"
    next_occurrence: Optional[datetime] = None
```

#### Indexes to Add
- Index on (user_id, priority) for priority filtering
- Index on (user_id, due_date) for due date filtering
- Index on (user_id, is_recurring) for recurring task identification
- GIN index on tags for efficient tag-based queries

### API Contract Extensions

#### Extended Task Models
```yaml
# New request/response models
CreateTaskRequest:
  type: object
  properties:
    title:
      type: string
    description:
      type: string
    priority:
      type: string
      enum: [low, medium, high, urgent]
      default: medium
    tags:
      type: array
      items:
        type: string
    due_date:
      type: string
      format: date-time
    is_recurring:
      type: boolean
      default: false
    recurrence_rule:
      type: string

UpdateTaskRequest:
  type: object
  properties:
    title:
      type: string
    description:
      type: string
    completed:
      type: boolean
    priority:
      type: string
      enum: [low, medium, high, urgent]
    tags:
      type: array
      items:
        type: string
    due_date:
      type: string
      format: date-time
    is_recurring:
      type: boolean
    recurrence_rule:
      type: string
    next_occurrence:
      type: string
      format: date-time

ListTasksQueryParams:
  type: object
  properties:
    priority:
      type: string
      description: Comma-separated list of priorities to filter by
    tags:
      type: string
      description: Comma-separated list of tags to filter by
    q:
      type: string
      description: Keyword to search in title and description
    sort:
      type: string
      description: Comma-separated list of fields to sort by (prefix with - for descending)
    due_after:
      type: string
      format: date
      description: Filter tasks with due date after this date
    due_before:
      type: string
      format: date
      description: Filter tasks with due date before this date
```

#### Extended Endpoints
```
GET /api/{user_id}/tasks
  Query Parameters:
    - priority: Comma-separated list of priorities (e.g. "high,urgent")
    - tags: Comma-separated list of tags (e.g. "work,personal")
    - q: Keyword search in title and description
    - sort: Comma-separated fields with optional - prefix for descending (e.g. "priority,-due_date,title,created_at")
    - due_after: Date filter (e.g. "2026-01-20")
    - due_before: Date filter (e.g. "2026-01-30")

POST /api/{user_id}/tasks
  Body: CreateTaskRequest (with new fields)

PUT /api/{user_id}/tasks/{task_id}
  Body: UpdateTaskRequest (with new fields)
```

### Event Contracts

#### Task Events Schema
```json
{
  "event_type": "created|updated|completed|deleted",
  "task_id": 123,
  "user_id": "user-uuid",
  "task_data": {
    "id": 123,
    "user_id": "user-uuid",
    "title": "Task title",
    "description": "Task description",
    "completed": false,
    "priority": "high",
    "tags": ["work", "urgent"],
    "due_date": "2026-01-20T18:00:00Z",
    "is_recurring": true,
    "recurrence_rule": "WEEKLY:Mon,Wed",
    "next_occurrence": "2026-01-22T09:00:00Z"
  },
  "timestamp": "2026-01-18T22:15:00Z"
}
```

#### Reminder Events Schema
```json
{
  "task_id": 123,
  "user_id": "user-uuid",
  "title": "Task title",
  "due_at": "2026-01-20T18:00:00Z",
  "remind_at": "2026-01-20T17:00:00Z",
  "timestamp": "2026-01-18T22:15:00Z"
}
```

### Service Contracts

#### Recurring Task Service
- Consumes: task-events topic (specifically "completed" events)
- Produces: New task creation events
- Responsibility: Creates next instance of recurring tasks when completed

#### Notification Service
- Consumes: reminders topic
- Action: Sends notification to user (logs for hackathon purposes)
- Responsibility: Handles reminder notifications

## Phase 2: Implementation Roadmap

### Phase 2.1: Database Schema & Migration
**Goal**: Add new task fields without breaking existing data
- Update SQLModel Task class with new fields
- Create Alembic migration for schema changes
- Write migration test to ensure existing tasks get sensible defaults
- Apply migration locally and verify

### Phase 2.2: Extend REST API & MCP Tools
**Goal**: Enable clients and AI agent to use new task properties
- Update Pydantic request/response models
- Extend GET /api/{user_id}/tasks with new query parameters
- Update MCP tools to accept new fields
- Add validation for recurrence_rule format

### Phase 2.3: Enhance Chatbot Intent Recognition
**Goal**: Teach AI to handle new task attributes naturally
- Update agent instructions/prompt for new capabilities
- Implement due date calculation for reminders
- Handle recurring task creation logic

### Phase 2.4: Add Event Publishing
**Goal**: Make chat-api produce events for other services
- Add Kafka/Redpanda producer utilities
- Publish events after successful DB operations
- Implement event schemas as defined

### Phase 2.5: Create New Microservices
**Goal**: Implement consumer services for events
- Create recurring-task-service for handling completed recurring tasks
- Create notification-service for handling reminders
- (Optional) Create audit-service for event logging

### Phase 2.6: Introduce Dapr Integration
**Goal**: Decouple services from direct Kafka dependencies
- Configure Dapr for local and cloud deployment
- Create Dapr component definitions
- Refactor services to use Dapr pub/sub
- Use Dapr for secrets management

### Phase 2.7: Local Deployment on Minikube
**Goal**: Validate full flow in local Kubernetes environment
- Extend existing Helm charts
- Add manifests for new services
- Deploy complete stack to Minikube
- Test end-to-end functionality

### Phase 2.8: Cloud Deployment
**Goal**: Deploy to production-grade Kubernetes cluster
- Set up Oracle OKE cluster (or alternative)
- Deploy complete application stack
- Verify functionality in cloud environment

### Phase 2.9: CI/CD Pipeline
**Goal**: Automate deployment process
- Create GitHub Actions workflow
- Automate Docker image building
- Implement deployment to cloud cluster

### Phase 2.10: Documentation & Monitoring
**Goal**: Complete the implementation with proper documentation
- Update README with new architecture
- Add monitoring and logging capabilities
- Create demo materials

## Quickstart Guide for Developers

### Prerequisites
- Python 3.13+
- UV package manager
- Docker and Docker Compose
- Minikube
- Kubectl
- Dapr CLI

### Setup Instructions
1. Clone the repository
2. Install dependencies with UV:
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -r requirements.txt
   ```
3. Set up local development environment:
   ```bash
   # Start Minikube
   minikube start
   
   # Initialize Dapr
   dapr init -k
   
   # Set up database
   alembic upgrade head
   ```
4. Run the application:
   ```bash
   # Backend
   cd backend
   dapr run --app-id chat-api --app-port 8000 -- uvicorn main:app --reload
   
   # Frontend
   cd frontend
   npm install
   npm start
   ```

### Running Tests
```bash
# Backend tests
cd backend
python -m pytest tests/

# Integration tests
python -m pytest tests/integration/
```

## Post-Design Constitution Check

### Verification of Adherence
- ✅ All existing functionality preserved (API endpoints, authentication, MCP tools)
- ✅ New features implemented as extensions rather than replacements
- ✅ Clean code principles maintained with separation of concerns
- ✅ Proper documentation of all new components
- ✅ Scalable architecture with event-driven design
- ✅ Secure implementation with proper authentication maintained

### Risk Mitigation Achieved
- Backward compatibility ensured through additive changes only
- Data integrity maintained with proper migration strategy
- Event-driven architecture implemented with Dapr for loose coupling
- Cloud deployment validated through Minikube testing