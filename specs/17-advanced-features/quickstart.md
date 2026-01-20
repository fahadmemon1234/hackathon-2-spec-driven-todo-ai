# Quickstart Guide: Advanced Todo App with Event-Driven Architecture

## Overview
This guide will help you set up and run the advanced Todo application with event-driven architecture using Kafka/Redpanda and Dapr.

## Prerequisites
- Python 3.13+
- UV package manager
- Docker and Docker Compose
- Minikube
- Kubectl
- Dapr CLI

## Setting Up the Environment

### 1. Clone the Repository
```bash
git clone <repository-url>
cd todo-app-Phase-5
```

### 2. Install Dependencies
```bash
# Create virtual environment with UV
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

### 3. Set Up Local Kubernetes Environment
```bash
# Start Minikube
minikube start

# Initialize Dapr on Minikube
dapr init -k

# Verify Dapr installation
dapr status -k
```

### 4. Set Up Redpanda (Kafka-compatible streaming platform)
```bash
# Create namespace for Redpanda
kubectl create namespace redpanda

# Add Redpanda Helm chart repository
helm repo add redpanda https://charts.redpanda.com
helm repo update

# Install Redpanda
helm install redpanda redpanda/redpanda --namespace redpanda

# Verify Redpanda is running
kubectl get pods -n redpanda
```

### 5. Set Up Database
```bash
# Run database migrations
alembic upgrade head
```

## Running the Application

### 1. Start the Backend Services
```bash
# Terminal 1: Start the main chat API with Dapr
cd backend
dapr run --app-id chat-api --app-port 8000 -- uvicorn main:app --reload

# Terminal 2: Start the recurring task service
dapr run --app-id recurring-task-service -- uvicorn services.recurring:app --reload

# Terminal 3: Start the notification service
dapr run --app-id notification-service -- uvicorn services.notification:app --reload
```

### 2. Start the Frontend
```bash
# Terminal 4: Start the React frontend
cd frontend
npm install
npm start
```

## Key Components

### Database Schema Changes
The Task model now includes:
- `priority`: Enum ("low", "medium", "high", "urgent")
- `tags`: JSON array of string tags
- `due_date`: DateTime when task is due
- `is_recurring`: Boolean indicating if task repeats
- `recurrence_rule`: String defining recurrence pattern
- `next_occurrence`: DateTime of next instance (for recurring tasks)

### New API Endpoints
- `GET /api/{user_id}/tasks` now supports query parameters:
  - `?priority=high,urgent` - Filter by priority
  - `?tags=work,personal` - Filter by tags
  - `?q=keyword` - Search in title and description
  - `?sort=priority,-due_date,title,created_at` - Sort by multiple fields
  - `?due_after=YYYY-MM-DD` & `?due_before=YYYY-MM-DD` - Date range filtering

### Event-Driven Architecture
- `task-events` topic: For task lifecycle events (created, updated, completed, deleted)
- `reminders` topic: For scheduling reminder notifications
- Dapr handles pub/sub communication between services

## Testing the Features

### 1. Create a Task with Advanced Properties
```bash
curl -X POST http://localhost:8000/api/user123/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Prepare presentation",
    "description": "Prepare slides for quarterly meeting",
    "priority": "high",
    "tags": ["work", "urgent"],
    "due_date": "2026-01-20T18:00:00Z",
    "is_recurring": true,
    "recurrence_rule": "FREQ=WEEKLY;BYDAY=MO,WE"
  }'
```

### 2. Filter Tasks
```bash
# Get high and urgent priority tasks
curl "http://localhost:8000/api/user123/tasks?priority=high,urgent"

# Get tasks with specific tags
curl "http://localhost:8000/api/user123/tasks?tags=work"

# Search tasks
curl "http://localhost:8000/api/user123/tasks?q=presentation"

# Sort tasks
curl "http://localhost:8000/api/user123/tasks?sort=priority,-due_date"
```

### 3. Complete a Recurring Task
When you mark a recurring task as complete, the system will automatically create the next instance based on the recurrence rule.

## Troubleshooting

### Common Issues
1. **Dapr not running**: Run `dapr status -k` to check Dapr components
2. **Redpanda not ready**: Check with `kubectl get pods -n redpanda`
3. **Database connection**: Ensure Neon PostgreSQL credentials are set in environment variables

### Useful Commands
```bash
# Check Dapr status
dapr status -k

# Check running pods
kubectl get pods

# View Dapr logs
kubectl logs -l app=dapr-placement-server -n dapr-system

# View application logs
kubectl logs -l app=chat-api
```

## Next Steps
1. Explore the Dapr dashboard: `dapr dashboard`
2. Monitor your event streams in Redpanda Console
3. Set up the CI/CD pipeline for cloud deployment
4. Review the monitoring and logging setup