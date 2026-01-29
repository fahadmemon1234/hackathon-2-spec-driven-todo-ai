# Tasks: Recurring Tasks Feature

**Feature**: Recurring Tasks for PremiumTask Application
**Author**: AF
**Date**: January 27, 2026
**Branch**: 1-recurring-tasks

## Overview

This document outlines the implementation tasks for the recurring tasks feature in the PremiumTask application. The feature allows users to create tasks that automatically generate new instances based on recurrence rules, using Kafka for event-driven architecture.

## Dependencies & Ordering

User Story 1 (Create Recurring Task) and User Story 2 (Complete Recurring Task) are tightly coupled and must be implemented together for a functional MVP. User Story 3 (View Recurring Task Indicators) can be implemented in parallel with US1 and US2. User Story 4 (Configure Recurrence Options) builds on US1. User Story 5 (Modify Existing Recurring Task) is dependent on all previous stories.

## Parallel Execution Opportunities

- T007 [P] [US1] and T010 [P] [US3] can be executed in parallel
- T008 [P] [US1] and T009 [P] [US2] can be executed in parallel

## Implementation Strategy

1. Start with the foundational database changes and model updates
2. Implement the core functionality for creating and completing recurring tasks
3. Add the Kafka integration for event-driven task generation
4. Enhance the frontend to support recurrence configuration and display
5. Add polish and error handling

---

## Phase 1: Setup

- [X] T001 Set up project dependencies for kafka-python and python-dateutil in requirements.txt
- [X] T002 Verify Kafka is running in docker-compose setup and 'task-events' topic exists

## Phase 2: Foundational

- [X] T003 Update Task model with recurrence fields: recurrence_rule, recurrence_end_date, recurrence_max_count, original_task_id, occurrence_number in backend/models/task.py
- [X] T004 Generate and apply Alembic migration for recurrence fields in backend/database/migrations/
- [X] T005 Create Kafka producer utility for publishing task events in backend/utils/kafka_producer.py
- [X] T006 Create RRULE utility functions for parsing and generating recurrence dates in backend/utils/recurrence_utils.py

## Phase 3: User Story 1 - Create Recurring Task (Priority: P1)

**Goal**: Enable users to create recurring tasks with various frequency options.

**Independent Test**: Can be fully tested by creating a recurring task with a specific frequency and verifying it appears in the task list with recurrence indicators.

- [X] T007 [P] [US1] Add recurrence form elements to task creation modal in frontend/src/components/TaskFormModal.tsx
- [X] T008 [P] [US1] Update task creation API endpoint to accept and store recurrence fields in backend/api/tasks.py
- [X] T009 [US1] Add validation for recurrence fields in backend/schemas/task.py
- [X] T010 [US1] Create helper function to convert UI recurrence options to RRULE format in backend/utils/recurrence_utils.py

## Phase 4: User Story 2 - Complete Recurring Task (Priority: P1)

**Goal**: When a recurring task is completed, automatically generate the next instance based on the recurrence rule.

**Independent Test**: Can be fully tested by completing a recurring task and verifying that a new instance is created with the appropriate due date.

- [X] T011 [US2] Update task completion endpoint to check for recurrence and publish Kafka event in backend/api/tasks.py
- [X] T012 [US2] Implement recurring task consumer to process completion events in services/recurring_consumer.py
- [X] T013 [US2] Add logic to generate next task instance based on recurrence rule in services/recurring_consumer.py
- [X] T014 [US2] Implement idempotency check to prevent duplicate task creation in services/recurring_consumer.py

## Phase 5: User Story 3 - View Recurring Task Indicators (Priority: P2)

**Goal**: Display visual indicators for recurring tasks so users know which tasks will automatically regenerate.

**Independent Test**: Can be fully tested by viewing tasks with recurrence indicators and confirming they display appropriately.

- [X] T015 [US3] Update task list component to show recurrence badges for recurring tasks in frontend/src/components/TaskList.tsx
- [X] T016 [US3] Add recurrence display property to task model for frontend consumption in backend/models/task.py
- [X] T017 [US3] Update task retrieval API to include recurrence indicators in backend/api/tasks.py

## Phase 6: User Story 4 - Configure Recurrence Options (Priority: P2)

**Goal**: Allow users to configure various recurrence options including end conditions.

**Independent Test**: Can be fully tested by configuring different recurrence options and verifying they are stored and applied correctly.

- [X] T018 [US4] Add end condition options ("End after" and "End on") to task creation modal in frontend/src/components/TaskFormModal.tsx
- [X] T019 [US4] Update task creation API to handle end conditions in backend/api/tasks.py
- [X] T020 [US4] Implement recurrence end condition checking in the consumer logic in services/recurring_consumer.py

## Phase 7: User Story 5 - Modify Existing Recurring Task (Priority: P3)

**Goal**: Allow users to modify recurrence settings of existing recurring tasks.

**Independent Test**: Can be fully tested by modifying recurrence settings and verifying they apply to future instances only.

- [X] T021 [US5] Update task edit modal to support modifying recurrence settings in frontend/src/components/TaskFormModal.tsx
- [X] T022 [US5] Update task update API endpoint to handle recurrence field changes in backend/api/tasks.py
- [X] T023 [US5] Ensure modification only affects future instances, not past ones in backend/services/task_service.py

## Phase 8: Polish & Cross-Cutting Concerns

- [X] T024 Add toast notification when next occurrence is created after completing recurring task in frontend/src/components/TaskList.tsx
- [X] T025 Add error handling and logging for recurrence operations in services/recurring_consumer.py
- [X] T026 Add consumer service to docker-compose.yml as recurring-consumer service
- [X] T027 Write integration tests for recurring task functionality in tests/integration/test_recurring_tasks.py
- [X] T028 Perform end-to-end testing: create recurring task → complete it → verify new instance created
- [X] T029 Document the recurring tasks feature in the README.md