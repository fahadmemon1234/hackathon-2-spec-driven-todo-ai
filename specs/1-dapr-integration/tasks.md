# Todo Application – Dapr Integration (Local Docker Compose) Tasks

## Feature Overview

This feature implements Dapr (Distributed Application Runtime) for the Todo Application backend using Docker Compose. The goal is to leverage Dapr's building blocks to enhance the application's capabilities with pub/sub messaging, state management, cron bindings, secrets management, and service invocation - all running locally without Kubernetes or cloud infrastructure.

## Implementation Strategy

- **MVP First**: Start with basic Dapr integration (pub/sub and state store) to establish the foundation
- **Incremental Delivery**: Add components one by one (pub/sub → state store → cron → secrets → service invocation)
- **Independent Testing**: Each user story should be testable in isolation
- **Parallel Execution**: Where possible, tasks are marked with [P] for parallel execution

## Dependencies

- User Story 1 (Pub/Sub) must be completed before User Story 2 (State Store) and User Story 4 (Reminders)
- User Story 2 (State Store) must be completed before User Story 3 (Cron Bindings)
- User Story 4 (Secrets) can be implemented in parallel with other stories but affects configuration of all components

## Parallel Execution Examples

- User Story 1: Tasks T020-T023 can be worked on in parallel with Tasks T024-T027
- User Story 2: State store implementation can be developed in parallel with reminder scheduling logic
- User Story 4: Secrets configuration can be implemented in parallel with other component configurations

---

## Phase 1: Setup (Project Initialization)

- [x] T001 Create components directory for Dapr component definitions in components/
- [x] T002 Install Dapr CLI and initialize Dapr runtime in standalone mode
- [x] T003 Verify Dapr installation with `dapr --version` and `dapr list`
- [x] T004 Update Docker Compose configuration to include Dapr sidecar for backend service in docker-compose.yml
- [x] T005 Verify Docker Compose configuration with `docker-compose config`

## Phase 2: Foundational (Blocking Prerequisites)

- [x] T010 Create Kafka pub/sub component definition in components/pubsub.yaml
- [x] T011 Create Redis state store component definition in components/statestore.yaml
- [x] T012 Create cron binding component definition in components/cron-binding.yaml
- [x] T013 Create secrets component definition in components/secrets.yaml
- [x] T014 Create secrets.json file with Kafka and Redis configuration
- [x] T015 Configure backend service with App ID "backend-service"
- [x] T016 Add Dapr client library to backend dependencies in backend/requirements.txt

## Phase 3: [US1] Dapr Pub/Sub Integration

**Goal**: Enable backend to publish and subscribe to Kafka topics via Dapr

**Independent Test Criteria**:
- Backend can publish messages to Kafka topics via Dapr HTTP API
- Backend can receive messages from Kafka topics via Dapr HTTP API
- Test messages appear in correct Kafka topics

**Tasks**:

- [x] T020 [P] [US1] Implement backend publish functions for task-events topic in backend/services/pubsub_service.py
- [x] T021 [P] [US1] Implement backend publish functions for reminders topic in backend/services/pubsub_service.py
- [x] T022 [P] [US1] Implement backend publish functions for task-updates topic in backend/services/pubsub_service.py
- [x] T023 [P] [US1] Map application events to appropriate Kafka topics in backend/event_mapper.py
- [x] T024 [P] [US1] Implement subscription endpoints in backend for task-updates topic in backend/routes/subscriptions.py
- [x] T025 [P] [US1] Implement subscription endpoints in backend for reminders topic in backend/routes/subscriptions.py
- [x] T026 [P] [US1] Implement subscription endpoints in backend for task-events topic in backend/routes/subscriptions.py
- [x] T027 [US1] Register subscriptions with Dapr in backend/dapr_config.py
- [x] T028 [US1] Handle incoming messages from Kafka appropriately in backend/message_handlers.py
- [x] T029 [US1] Send test message and verify it appears in Kafka topic via Dapr API
- [x] T030 [US1] Publish test message and verify backend receives it via subscription

## Phase 4: [US2] Dapr State Store Integration

**Goal**: Enable backend to save and retrieve state via Dapr state store

**Independent Test Criteria**:
- Backend can save task state to Redis via Dapr HTTP API
- Backend can retrieve task state from Redis via Dapr HTTP API
- State persists correctly with proper key structure

**Tasks**:

- [x] T040 [P] [US2] Implement save state functions using Dapr HTTP API in backend/services/state_service.py
- [x] T041 [P] [US2] Implement retrieve state functions using Dapr HTTP API in backend/services/state_service.py
- [x] T042 [P] [US2] Implement delete state functions using Dapr HTTP API in backend/services/state_service.py
- [x] T043 [US2] Define key patterns for task state: `task:{taskId}` in backend/constants.py
- [x] T044 [US2] Define key patterns for recurrence metadata: `recurrence:{taskId}` in backend/constants.py
- [x] T045 [US2] Define key patterns for reminder schedules: `reminder:{reminderId}` in backend/constants.py
- [x] T046 [US2] Integrate state operations with task creation in backend/routes/tasks.py
- [x] T047 [US2] Integrate state operations with task retrieval in backend/routes/tasks.py
- [x] T048 [US2] Integrate state operations with task updates in backend/routes/tasks.py
- [x] T049 [US2] Save and retrieve test data via Dapr state API
- [x] T050 [US2] Verify state key structure follows defined patterns

## Phase 5: [US3] Dapr Cron Bindings (Reminders)

**Goal**: Enable scheduled reminder processing via Dapr cron binding

**Independent Test Criteria**:
- Cron binding triggers at specified intervals
- Backend processes scheduled reminders when triggered
- Reminder events are published to Kafka via pub/sub

**Tasks**:

- [x] T060 [US3] Create endpoint that Dapr will invoke on schedule in backend/routes/reminders.py
- [x] T061 [US3] Implement logic to check for due reminders in backend/services/reminder_service.py
- [x] T062 [US3] Implement logic to publish reminder events to Kafka via pub/sub in backend/services/reminder_service.py
- [x] T063 [US3] Store reminder schedule in state store via Dapr API in backend/services/reminder_service.py
- [x] T064 [US3] Retrieve reminder schedule from state store via Dapr API in backend/services/reminder_service.py
- [x] T065 [US3] Trigger cron manually and verify reminder processing
- [x] T066 [US3] Schedule a test reminder and verify it processes correctly
- [x] T067 [US3] Verify reminder event published to Kafka when cron triggers

## Phase 6: [US4] Dapr Secrets Integration

**Goal**: Enable backend to read configuration from Dapr secrets

**Independent Test Criteria**:
- Backend retrieves Kafka configuration via Dapr secrets API
- Backend retrieves Redis configuration via Dapr secrets API
- Configuration is properly applied to respective services

**Tasks**:

- [x] T080 [US4] Implement secret retrieval functions using Dapr HTTP API in backend/services/secret_service.py
- [x] T081 [US4] Replace hardcoded Kafka configuration with Dapr secret calls in backend/config.py
- [x] T082 [US4] Replace hardcoded Redis configuration with Dapr secret calls in backend/config.py
- [x] T083 [US4] Update configuration loading logic to use Dapr secrets in backend/main.py
- [x] T084 [US4] Verify backend starts and operates using secrets from Dapr
- [x] T085 [US4] Verify Kafka connection uses configuration from secrets
- [x] T086 [US4] Verify Redis connection uses configuration from secrets

## Phase 7: [US5] Dapr Service Invocation

**Goal**: Enable internal service-to-service calls using Dapr

**Independent Test Criteria**:
- Service invocation works between backend services
- Requests and responses are handled properly
- Backend endpoints are accessible via Dapr service invocation

**Tasks**:

- [x] T090 [US5] Create endpoints that follow Dapr service invocation patterns in backend/routes/internal.py
- [x] T091 [US5] Implement appropriate request/response handling for service invocation in backend/handlers/service_invocation.py
- [x] T092 [US5] Make test calls between services using Dapr service invocation in backend/tests/service_invocation_test.py
- [x] T093 [US5] Verify request/response handling works correctly
- [x] T094 [US5] Invoke backend endpoints via Dapr service invocation and verify response

## Phase 8: [US6] End-to-End Event Flows

**Goal**: Implement and test complete event flows using multiple Dapr components

**Independent Test Criteria**:
- Task creation flow works end-to-end with state store and pub/sub
- Reminder scheduling flow works end-to-end with state store, cron, and pub/sub
- Recurring task processing flow works end-to-end with all components

**Tasks**:

- [x] T100 [P] [US6] Implement task creation flow: store task in state store → publish "task-created" event in backend/workflows/task_creation.py
- [x] T101 [P] [US6] Implement reminder scheduling flow: store reminder in state store → cron triggers → publish reminder notification in backend/workflows/reminder_flow.py
- [x] T102 [P] [US6] Implement recurring task processing: store recurrence metadata → cron triggers → create new task → publish event in backend/workflows/recurring_tasks.py
- [x] T103 [US6] Test complete task creation flow from frontend to Kafka
- [x] T104 [US6] Test complete reminder scheduling flow from creation to notification
- [x] T105 [US6] Test complete recurring task processing flow

## Phase 9: Testing & Validation

**Goal**: Ensure all components work together reliably

**Independent Test Criteria**:
- All smoke tests pass successfully
- System handles failure scenarios gracefully
- System recovers properly after restarts
- Proper logging is in place

**Tasks**:

- [x] T110 [P] Create tests that exercise pub/sub functionality in backend/tests/test_pubsub.py
- [x] T111 [P] Create tests that exercise state store functionality in backend/tests/test_state_store.py
- [x] T112 [P] Create tests that exercise cron binding functionality in backend/tests/test_cron.py
- [x] T113 [P] Create tests that exercise secrets functionality in backend/tests/test_secrets.py
- [x] T114 [P] Create tests that exercise service invocation functionality in backend/tests/test_service_invocation.py
- [x] T115 Test behavior when Kafka is unavailable and implement error handling in backend/error_handlers.py
- [x] T116 Test behavior when Redis is unavailable and implement error handling in backend/error_handlers.py
- [x] T117 Test behavior when Dapr sidecar is unavailable and implement error handling in backend/error_handlers.py
- [x] T118 Restart Docker Compose stack and verify functionality preservation
- [x] T119 Verify state persistence across restarts
- [x] T120 Verify Dapr sidecar logs are accessible and informative
- [x] T121 Verify backend logs include Dapr interactions
- [x] T122 Run comprehensive smoke test suite and verify all tests pass

## Phase 10: Documentation & Readiness

**Goal**: Document the implementation and prepare for future enhancements

**Independent Test Criteria**:
- Documentation is clear and accurate
- Known limitations are clearly communicated
- Ready-for-cloud checklist is comprehensive

**Tasks**:

- [x] T130 Update README with Dapr setup instructions in README.md
- [x] T131 Document component configurations in docs/dapr-components.md
- [x] T132 Document common troubleshooting steps in docs/troubleshooting.md
- [x] T133 Identify and document any limitations in docs/limitations.md
- [x] T134 Note areas for future improvement in docs/future-improvements.md
- [x] T135 Create checklist of items needed for cloud deployment in docs/cloud-readiness.md
- [x] T136 Include considerations for production environments in docs/production-notes.md
- [x] T137 Note differences between local and cloud configurations in docs/local-vs-cloud.md