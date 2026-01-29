# Recurring Tasks Feature - Execution Plan (sp.plan)

## 1. Overview & Assumptions
This plan implements recurring tasks functionality in the PremiumTask application using Kafka for event-driven architecture. When users complete a recurring task, the system will automatically generate the next instance based on the recurrence rule. The implementation will include database schema updates, backend API changes, Kafka integration, and frontend UI enhancements.

Assumptions: Existing FastAPI backend with SQLModel/PostgreSQL, docker-compose has kafka/zookeeper/postgres, topic 'task-events' exists, frontend is React/TSX-like with modal.

## 2. Prerequisites
- Tools/versions: Python 3.11+, pip packages (fastapi, sqlmodel, alembic, confluent-kafka or kafka-python, python-dateutil, uvicorn)
- Pre-check commands: docker ps shows postgres/kafka up
- Existing: Task model, task CRUD endpoints, Kafka setup with 'task-events' topic

## 3. Step-by-Step Implementation Tasks

### Task 1: Database Schema Update (Add Recurrence Fields)
1. Update the Task model in the backend to include recurrence fields:
   - recurrence_rule: str | None (RRULE string e.g. "FREQ=DAILY;INTERVAL=1")
   - recurrence_end_date: datetime | None (optional end date)
   - recurrence_max_count: int | None (max occurrences)
   - original_task_id: int | None (foreign key to parent Task.id)
   - occurrence_number: int = 1 (1 = original, 2 = first repeat, etc.)
2. Generate Alembic migration:
   - Commands: alembic revision --autogenerate -m "add recurrence fields"
   - Apply migration: alembic upgrade head
3. Verify: Check DB table schema (psql or pgAdmin)

### Task 2: Update SQLModel Task Class
1. Add new fields to Task model (include Optional typing)
2. Import necessary types (Optional, datetime)
3. Add relationship if needed for original_task_id (back_populates optional)
4. Verify: Restart backend, no model errors

### Task 3: Frontend UI Updates (Recurring in Create/Refine Modal)
1. Add checkbox "Make this task recurring" (default: unchecked)
2. Conditional: show dropdown with options: Daily, Weekly, Monthly, Yearly
3. Map selection to RRULE strings (e.g. "FREQ=DAILY", "FREQ=WEEKLY")
4. (Optional) Add end conditions: "End after" (number) and "End on" (date picker)
5. Update form payload to send recurrence_rule to backend
6. Display recurrence badge on task cards (e.g. "Repeats daily")
7. Verify: Open modal → toggle → see dropdown → save task

### Task 4: Backend - Task Completion Endpoint with Producer
1. Update PATCH /tasks/{task_id}/complete endpoint
2. Mark task.status = "completed"
3. If task.recurrence_rule exists:
   - Use confluent-kafka (or kafka-python) Producer to send JSON event to 'task-events'
   - Event: {"event_type": "task_completed", "task_id": ..., "recurrence_rule": ..., "title": ..., "due_date": ..., "description": ..., "urgency": ..., "tags": ..., "user_id": ..., "original_task_id": ..., "occurrence_number": ...}
4. Use dependency for Kafka producer (lifespan or per-request)
5. Verify: curl complete endpoint → check Kafka (console-consumer) sees event

### Task 5: Implement Recurring Task Consumer
1. Create new file: services/recurring_consumer.py
2. Use kafka-python or confluent-kafka Consumer
3. Subscribe to 'task-events'
4. On message: if event_type=="task_completed" and recurrence_rule:
   - Parse rrulestr(recurrence_rule).after(completed_date or current due)
   - Create new Task: copy fields, set due_date=next, original_task_id=old.id, occurrence_number +=1, status="pending"
   - Insert via SQLModel session (async if possible)
   - Idempotency: check if similar task (original_id + due_date) exists → skip
5. Logging: print or structlog
6. Run as: python services/recurring_consumer.py
7. Verify: Produce test event → see new task in DB

### Task 6: Add Consumer to docker-compose.yml
1. New service: recurring-consumer
   - build: . (or image from Dockerfile)
   - command: python services/recurring_consumer.py
   - depends_on: [db, kafka]
   - environment: same DB/KAFKA env vars
2. Restart stack: docker-compose up -d
3. Verify: docker logs recurring-consumer shows "Connected to Kafka"

### Task 7: End-to-End Testing & Polish
1. Test flow: Create recurring daily task → complete it → check DB for new task with +1 day due_date
2. Edge cases: No recurrence → no event; Invalid RRULE → log error; End date reached → no new task
3. Add badge in frontend task list for recurring tasks
4. Show toast notification "Next occurrence created" when completing recurring tasks
5. Manual: kafka-console-producer for simulation

## 4. Dependencies & Ordering (Text Graph)
Task 1 → Task 2 → Task 4 → Task 5 → Task 6
Task 1 → Task 2 → Task 3 (frontend parallel)

## 5. Risks & Mitigations
- Risk 1: RRULE parsing fails (invalid string) → Mitigation: Validate on create, catch exceptions in consumer
- Risk 2: Consumer crashes on DB error → Mitigation: Retry logic (confluent retry config), dead-letter topic later
- Risk 3: Duplicate events create duplicates → Mitigation: Idempotency check before insert
- Risk 4: Timezone issues in dates → Mitigation: Use UTC everywhere, aware datetimes
- Risk 5: Consumer not starting (env vars) → Mitigation: Healthcheck or logs
- Risk 6: Race conditions when multiple consumers process same event → Mitigation: Proper partitioning and idempotency

## 6. Success Criteria Checklist
- [ ] Alembic migration applied, new columns in tasks table
- [ ] Create/edit task with recurrence → saved as RRULE
- [ ] Complete recurring task → event in Kafka
- [ ] Consumer processes event → new task in DB with next due_date
- [ ] New task visible in UI, original marked completed
- [ ] No duplicates on re-processing event
- [ ] docker logs show clean consumer operation
- [ ] Frontend shows recurrence indicators
- [ ] Toast notification appears when completing recurring tasks

## 7. Estimated Effort
- Task 1–2: 20–30 min
- Task 3: 20–40 min (frontend)
- Task 4: 30 min
- Task 5: 40–60 min
- Task 6–7: 20–30 min
- Total: 2–3 hours (with testing)

## 8. Next Steps After Success
- Integrate reminders (similar consumer for 'reminders' topic)
- Add UI for viewing recurrence series / stop recurrence
- Move consumer to FastAPI lifespan or dedicated microservice
- Add metrics (how many recurrences generated)