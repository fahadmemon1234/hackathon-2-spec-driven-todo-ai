# Quickstart Guide: Recurring Tasks Feature

## Overview
This guide explains how to set up and use the recurring tasks feature in the PremiumTask application. The feature allows users to create tasks that automatically generate new instances based on recurrence rules.

## Prerequisites
- Docker and Docker Compose installed
- Python 3.11+
- Kafka cluster running (included in docker-compose setup)

## Setup Instructions

### 1. Environment Setup
```bash
# Clone the repository
git clone <repository-url>
cd todo-app-Phase-5

# Install dependencies
uv sync  # or pip install -r requirements.txt
```

### 2. Database Migration
```bash
# Apply the recurring tasks migration
alembic revision --autogenerate -m "add recurrence fields"
alembic upgrade head
```

### 3. Start Services
```bash
# Start all services including Kafka and the recurring task consumer
docker-compose up -d
```

### 4. Verify Setup
```bash
# Check that all services are running
docker-compose ps

# Verify the consumer is connected to Kafka
docker logs recurring-consumer
```

## Usage Instructions

### Creating a Recurring Task
1. Navigate to the task creation form
2. Fill in the task details (title, description, due date, etc.)
3. Check the "Make this task recurring" checkbox
4. Select a recurrence frequency (Daily, Weekly, Monthly, Yearly)
5. Optionally set end conditions ("End after X occurrences" or "End on date")
6. Save the task

### Completing a Recurring Task
1. Find the recurring task in your task list
2. Mark the task as completed using the completion button/checkmark
3. The system will automatically generate the next instance of the task
4. You'll see a toast notification: "Next occurrence created"
5. The original task will be marked as completed, and the new instance will appear in your task list

### Identifying Recurring Tasks
- Recurring tasks display a badge or indicator showing their recurrence pattern (e.g., "Repeats daily")
- Completed recurring tasks remain in your history for reference

## Testing the Feature
```bash
# Manually trigger a recurring task completion
curl -X PATCH http://localhost:8000/api/tasks/1/complete

# Verify the new task instance was created
curl -X GET http://localhost:8000/api/tasks/

# Check Kafka for the task completion event
docker exec -it kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic task-events --from-beginning
```

## Troubleshooting
- If the recurring task consumer isn't creating new tasks:
  - Check that Kafka is running: `docker-compose ps`
  - Verify the consumer logs: `docker logs recurring-consumer`
  - Ensure the task has a valid recurrence_rule
- If the database migration fails:
  - Check that the database is accessible
  - Verify the migration file contains the correct schema changes
- If the UI doesn't show recurrence options:
  - Verify the frontend code includes the recurrence form elements
  - Check browser console for JavaScript errors