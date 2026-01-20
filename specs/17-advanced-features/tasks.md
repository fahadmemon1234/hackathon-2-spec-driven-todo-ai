# Tasks: Advanced Features, Event-Driven Architecture and Cloud Deployment

**Feature**: Advanced Features, Event-Driven Architecture and Cloud Deployment
**Feature Branch**: 17-advanced-features
**Created**: 2026-01-19
**Status**: Draft

## Dependencies & Execution Order

### User Story Dependency Graph
- US1 (Enhanced Task Management) → No dependencies
- US2 (Recurring Tasks) → Depends on US1 (needs enhanced task model)
- US3 (Task Reminders) → Depends on US1 (needs due_date field)
- US4 (Event-Driven Architecture) → Depends on US1, US2, US3 (events for all features)
- US5 (Cloud Deployment) → Depends on US4 (deploy all services)

### Parallel Execution Opportunities
- Within each user story, model, service, and endpoint implementations can often run in parallel
- Infrastructure setup (Dapr, Redpanda) can happen in parallel with service development
- Unit tests can be written in parallel with implementation

## Implementation Strategy

### MVP Scope
- Start with US1 (Enhanced Task Management) as the core MVP
- This provides immediate user value with priority, tags, and due dates
- Subsequent stories build upon this foundation

### Incremental Delivery
- Each user story delivers independent value
- Maintain backward compatibility at each step
- Test each increment before moving to the next

## Phase 1: Setup (Project Initialization)

### Goal
Prepare the development environment and initialize project structure for advanced features.

### Independent Test Criteria
- Development environment is set up with all required dependencies
- Base project structure is in place
- Initial configurations are established

### Tasks

- [X] T001 Set up development environment with Python 3.13+, UV, Docker, Minikube, Kubectl, Dapr CLI
- [X] T002 Create directory structure for new services (recurring-task-service, notification-service)
- [X] T003 Update requirements.txt with new dependencies (kafka-python, dapr-ext, dateutil)
- [X] T004 Configure Alembic for database migrations
- [X] T005 Set up Dapr configuration for local development

## Phase 2: Foundational (Blocking Prerequisites)

### Goal
Implement foundational components that all user stories depend on.

### Independent Test Criteria
- Database schema is extended with new fields
- Core models are updated to support new features
- Basic event publishing infrastructure is in place

### Tasks

- [X] T006 [P] Update Task SQLModel with new fields: priority, tags, due_date, is_recurring, recurrence_rule, next_occurrence
- [X] T007 Create Alembic migration for database schema changes
- [X] T008 [P] Implement recurrence rule parsing utility using dateutil.rrule
- [X] T009 [P] Set up Kafka/Redpanda connection utilities
- [X] T010 [P] Create event schemas for task-events and reminders
- [X] T011 Update Pydantic models for API requests/responses with new fields
- [X] T012 Apply database migration and verify schema changes
- [X] T013 [P] Create base event publisher utility class

## Phase 3: User Story 1 - Enhanced Task Management (Priority: P1)

### Goal
Enable users to add priority levels, tags, and due dates to their tasks for better organization and management.

### Independent Test Criteria
- Can create tasks with priority, tags, and due dates
- Tasks display correctly in the UI with new attributes
- Filtering by priority and tags works correctly

### Acceptance Scenarios
1. Given I am logged into the Todo app, When I create a task with priority, tags, and due date, Then the task is saved with these attributes and displayed correctly
2. Given I have tasks with different priorities and tags, When I filter tasks by priority or tags, Then only matching tasks are displayed

### Tasks

- [X] T014 [P] [US1] Update CreateTaskRequest Pydantic model with new fields
- [X] T015 [P] [US1] Update UpdateTaskRequest Pydantic model with new fields
- [X] T016 [P] [US1] Update TaskResponse Pydantic model with new fields
- [X] T017 [US1] Extend GET /api/{user_id}/tasks with priority filtering
- [X] T018 [US1] Extend GET /api/{user_id}/tasks with tags filtering
- [X] T019 [US1] Extend GET /api/{user_id}/tasks with due date range filtering
- [X] T020 [US1] Extend GET /api/{user_id}/tasks with keyword search (q parameter)
- [X] T021 [US1] Extend GET /api/{user_id}/tasks with sorting capabilities
- [X] T022 [US1] Update POST /api/{user_id}/tasks to accept new fields
- [X] T023 [US1] Update PUT /api/{user_id}/tasks/{task_id} to update new fields
- [X] T024 [US1] Update add_task MCP tool to accept new fields
- [X] T025 [US1] Update update_task MCP tool to accept new fields
- [X] T026 [US1] Update list_tasks MCP tool to support new filters and sorting
- [X] T027 [US1] Add validation for recurrence_rule format in models
- [X] T028 [US1] Update database queries to support new filters and sorting
- [ ] T029 [US1] Update frontend to display and edit new task fields
- [ ] T030 [US1] Test enhanced task creation and filtering functionality

## Phase 4: User Story 2 - Recurring Tasks (Priority: P2)

### Goal
Enable users to create recurring tasks so they don't have to manually recreate repetitive tasks.

### Independent Test Criteria
- Can create recurring tasks with recurrence rules
- When a recurring task is completed, the next instance is automatically created
- Recurring tasks can be distinguished from regular tasks

### Acceptance Scenarios
1. Given I have created a recurring task, When I mark it as complete, Then the system creates the next instance according to the recurrence rule
2. Given I have recurring tasks, When I view my tasks, Then I can distinguish recurring tasks from regular tasks

### Tasks

- [X] T031 [P] [US2] Create RecurringTaskService class to handle recurring logic
- [X] T032 [US2] Implement calculate_next_occurrence function using dateutil.rrule
- [X] T033 [US2] Update task completion logic to handle recurring tasks
- [X] T034 [US2] Create function to generate next task instance from recurring task
- [X] T035 [US2] Add database query to find and process completed recurring tasks
- [ ] T036 [US2] Update frontend to show recurring task indicators
- [ ] T037 [US2] Add recurrence rule validation in the UI
- [ ] T038 [US2] Test recurring task creation and next instance generation
- [ ] T039 [US2] Test recurrence rule parsing and calculation accuracy

## Phase 5: User Story 3 - Task Reminders (Priority: P3)

### Goal
Provide reminder notifications for tasks with due dates so users don't miss important deadlines.

### Independent Test Criteria
- When a task with a due date is created, a reminder event is scheduled
- Reminder notifications are triggered at the appropriate time
- Users can see upcoming reminders

### Acceptance Scenarios
1. Given I have a task with a due date, When the due date approaches, Then I receive a reminder notification
2. Given I have multiple tasks with upcoming due dates, When I check my notifications, Then I see all relevant reminders

### Tasks

- [X] T040 [P] [US3] Create ReminderService class to handle reminder scheduling
- [X] T041 [US3] Implement calculate_reminder_time function (typically due_date - 1 hour)
- [X] T042 [US3] Update task creation to schedule reminder events
- [X] T043 [US3] Update task modification to reschedule reminder events if due_date changes
- [X] T044 [US3] Create reminder event schema and publisher
- [X] T045 [US3] Add reminder scheduling to add_task MCP tool
- [X] T046 [US3] Add reminder rescheduling to update_task MCP tool
- [ ] T047 [US3] Update frontend to show reminder indicators
- [ ] T048 [US3] Test reminder scheduling and notification functionality
- [ ] T049 [US3] Test reminder rescheduling when due dates change

## Phase 6: User Story 4 - Event-Driven Architecture (Priority: P4)

### Goal
Implement event-driven communication between services using Kafka/Redpanda and Dapr.

### Independent Test Criteria
- Task events (create, update, complete, delete) are published to the task-events topic
- Reminder events are published to the reminders topic
- Services can consume events from the event streams
- Event-driven architecture scales independently

### Acceptance Scenarios
1. Given a task is created/updated/completed/deleted, When the action occurs, Then the corresponding event is published to the task-events topic
2. Given reminder events are published, When the notification service is running, Then it processes the events and sends appropriate notifications

### Tasks

- [X] T050 [P] [US4] Set up Dapr pub/sub component configuration for Kafka/Redpanda
- [X] T051 [US4] Create recurring-task-service FastAPI application
- [X] T052 [US4] Create notification-service FastAPI application
- [X] T053 [US4] Implement event publishing in chat-api for task operations
- [X] T054 [US4] Implement event publishing in chat-api for reminder scheduling
- [X] T055 [US4] Implement recurring-task-service to consume task-events
- [X] T056 [US4] Implement notification-service to consume reminder events
- [X] T057 [US4] Update chat-api to use Dapr pub/sub instead of direct Kafka client
- [X] T058 [US4] Update recurring-task-service to use Dapr pub/sub
- [X] T059 [US4] Update notification-service to use Dapr pub/sub
- [X] T060 [US4] Set up Dapr secret store for Kafka credentials and DB URL
- [ ] T061 [US4] Test event publishing and consumption between services
- [ ] T062 [US4] Test end-to-end recurring task workflow via events
- [ ] T063 [US4] Test end-to-end reminder notification workflow via events

## Phase 7: User Story 5 - Cloud Deployment (Priority: P5)

### Goal
Deploy the application to a Kubernetes cluster with all services operational.

### Independent Test Criteria
- All services successfully deploy to Kubernetes cluster
- Services communicate properly via Dapr and event streams
- Application functions as expected in cloud environment

### Acceptance Scenarios
1. Given Kubernetes cluster resources, When I deploy the application using Helm charts, Then all services start successfully and communicate properly
2. Given deployed application, When I access the UI and API, Then they function as expected

### Tasks

- [ ] T064 [P] [US5] Create Helm chart for recurring-task-service
- [ ] T065 [P] [US5] Create Helm chart for notification-service
- [ ] T066 [US5] Update existing Helm charts to include new services
- [ ] T067 [US5] Create Dapr component definitions for Kubernetes
- [ ] T068 [US5] Create Kubernetes manifest for Redpanda deployment
- [ ] T069 [US5] Set up Oracle OKE cluster (or alternative)
- [ ] T070 [US5] Install Dapr on cloud Kubernetes cluster
- [ ] T071 [US5] Deploy application to cloud cluster using Helm
- [ ] T072 [US5] Test end-to-end functionality in cloud environment
- [ ] T073 [US5] Verify all services are operational and communicating
- [ ] T074 [US5] Set up basic monitoring and logging in cloud

## Phase 8: Polish & Cross-Cutting Concerns

### Goal
Complete the implementation with proper documentation, monitoring, and final touches.

### Independent Test Criteria
- README is updated with new architecture and setup instructions
- Monitoring and logging are properly configured
- All features work together seamlessly

### Tasks

- [ ] T075 Update README with new architecture diagram and setup instructions
- [ ] T076 Document new features and how to use them
- [ ] T077 Add health checks to all services
- [ ] T078 Set up basic monitoring for services
- [ ] T079 Create CI/CD pipeline for automated deployments
- [ ] T080 Perform end-to-end testing of all features
- [ ] T081 Document troubleshooting guide
- [ ] T082 Create demo materials and record demonstration
- [ ] T083 Final integration testing on cloud deployment
- [ ] T084 Prepare handoff documentation for maintenance