# PremiumTask - Advanced Todo Application with Dapr Integration

Welcome to PremiumTask, an advanced todo application built with modern technologies including Next.js, FastAPI, PostgreSQL, Kafka for event-driven architecture, and Dapr (Distributed Application Runtime) for enhanced microservices capabilities.

## Minikube Deployment

This application can also be deployed using Minikube for local Kubernetes development. Follow these steps to deploy the application to a local Minikube cluster:

1. Ensure you have Minikube, kubectl, and Dapr CLI installed
2. Start Minikube with sufficient resources:
   ```bash
   minikube start --driver=docker --memory=6144mb --cpus=4
   ```
3. Install Dapr in Kubernetes mode:
   ```bash
   dapr init -k
   ```
4. Build and load application images into Minikube:
   ```bash
   # Build images
   docker build -f Dockerfile.backend -t todo-app-backend:minikube .
   docker build -f Dockerfile.frontend -t todo-app-frontend:minikube .

   # Load images into Minikube
   minikube image load todo-app-backend:minikube
   minikube image load todo-app-frontend:minikube
   ```
5. Apply Kubernetes manifests:
   ```bash
   kubectl apply -f k8s/namespace.yaml
   kubectl apply -f k8s/configmap.yaml
   kubectl apply -f k8s/pvc.yaml
   kubectl apply -f k8s/postgres-deployment.yaml
   kubectl apply -f k8s/postgres-service.yaml
   kubectl apply -f k8s/redis-deployment.yaml
   kubectl apply -f k8s/redis-service.yaml
   kubectl apply -f k8s/zookeeper-deployment.yaml
   kubectl apply -f k8s/zookeeper-service.yaml
   kubectl apply -f k8s/kafka-deployment.yaml
   kubectl apply -f k8s/kafka-service.yaml
   kubectl apply -f k8s/dapr-components/
   kubectl apply -f k8s/backend-deployment.yaml
   kubectl apply -f k8s/backend-service.yaml
   kubectl apply -f k8s/frontend-deployment.yaml
   kubectl apply -f k8s/frontend-service.yaml
   kubectl apply -f k8s/recurring-consumer-deployment.yaml
   ```
6. Access the application:
   ```bash
   minikube service frontend --namespace todo-app
   ```

## Dapr Integration Features

PremiumTask now includes Dapr (Distributed Application Runtime) integration, providing the following capabilities:

- **Pub/Sub Messaging**: Using Kafka for event-driven communication between services
- **State Management**: Using Redis for persistent state storage
- **Cron Bindings**: For scheduled tasks like reminder processing
- **Secrets Management**: Secure configuration management
- **Service Invocation**: For internal service-to-service communication

## Recurring Tasks Feature

PremiumTask now includes a powerful recurring tasks feature that allows users to create tasks that automatically generate new instances based on recurrence rules.

### Features

- **Create Recurring Tasks**: Set up tasks to repeat daily, weekly, monthly, or yearly
- **End Conditions**: Specify when recurring tasks should stop (after X occurrences or on a specific date)
- **Visual Indicators**: Clear badges and icons to identify recurring tasks in your task list
- **Automatic Generation**: When you complete a recurring task, the next instance is automatically created based on the recurrence rule
- **History Preservation**: Completed recurring tasks remain in your history for reference

### How to Use

#### Creating a Recurring Task

1. Click the "New Objective" button to open the task creation modal
2. Fill in the task details (title, description, priority, etc.)
3. Check the "Recurring Task" checkbox
4. Select the recurrence frequency (Daily, Weekly, Monthly, Yearly)
5. Optionally set an end condition:
   - "End after": Specify the number of occurrences
   - "End on": Select a specific end date
6. Save the task

#### Managing Recurring Tasks

- When you mark a recurring task as complete, the system will automatically generate the next instance based on the recurrence rule
- Completed recurring tasks remain in your task list for historical reference
- You can edit the recurrence settings of existing recurring tasks

### Technical Architecture

The recurring tasks feature is implemented using an event-driven architecture:

- When a recurring task is completed, the backend publishes a "task_completed" event to the "task-events" Kafka topic
- A dedicated recurring task consumer service listens to this topic
- When a completion event is received, the consumer calculates the next occurrence date based on the recurrence rule
- The consumer then creates a new task instance with the appropriate due date and increments the occurrence counter
- The system includes idempotency checks to prevent duplicate task creation

### Configuration

The recurring task consumer service is configured in the docker-compose.yml file and connects to both the PostgreSQL database and Kafka cluster.

## Dapr Setup Instructions

### Prerequisites

- Docker and Docker Compose
- Dapr CLI installed and initialized
- Python 3.8+

### Installation Steps

1. **Install Dapr CLI and Initialize Runtime**:
   ```bash
   # On Windows with Chocolatey
   choco install dapr

   # Or follow installation instructions at https://docs.dapr.io/getting-started/install-dapr-cli/

   # Initialize Dapr in standalone mode
   dapr init
   ```

2. **Clone and Navigate to Project**:
   ```bash
   git clone <repository-url>
   cd todo-app-Phase-5
   ```

3. **Start the Application with Dapr**:
   ```bash
   docker-compose up -d
   ```

4. **Verify Dapr Components**:
   ```bash
   # Check if Dapr sidecar is running
   dapr list

   # Check component health
   docker-compose logs dapr-sidecar
   ```

### Dapr Components Configuration

The application uses the following Dapr components located in the `components/` directory:

- `pubsub.yaml`: Kafka pub/sub configuration
- `statestore.yaml`: Redis state store configuration
- `cron-binding.yaml`: Cron binding for scheduled tasks
- `secrets.yaml`: Secrets store configuration

### Available Services

- **Backend API**: Running on `http://localhost:8000`
- **Dapr Sidecar**: Available on `http://localhost:3500`
- **Frontend**: Running on `http://localhost:3001`
- **Kafka**: Available on `localhost:9092`
- **Redis**: Available on `localhost:6379`
- **PostgreSQL**: Available on `localhost:5432`

### Testing Dapr Integration

You can test the Dapr integration using the Dapr CLI:

```bash
# Publish a test event to Kafka via Dapr
curl -X POST http://localhost:3500/v1.0/publish/kafka-pubsub/task-events -H "Content-Type: application/json" -d '{"taskId": "test-123", "action": "created"}'

# Save state via Dapr
curl -X POST http://localhost:3500/v1.0/state/statestore -H "Content-Type: application/json" -d '[{ "key": "task:test-123", "value": {"title": "Test Task", "status": "pending"}}]'

# Get state via Dapr
curl http://localhost:3500/v1.0/state/statestore/task:test-123
```

---

## Key Features

* Create tasks with title, description, priority, and tags
* View tasks with clear status indicators and priority icons
* Mark tasks as complete or incomplete
* Update task details, priority, and tags
* Delete tasks by ID
* Search tasks by keyword across title, description, and tags
* Filter tasks by status, priority, or tag
* Sort tasks by priority, status, or title
* Strong input validation and user-friendly error messages

---

## Requirements

* Python 3.13 or higher
* UV package manager

---

## Setup Instructions

1. Verify Python installation:

   ```bash
   python --version
   ```

2. Install UV (if not already installed):

   ```bash
   pip install uv
   ```

3. Navigate to the project root directory

4. Install dependencies:

   ```bash
   uv sync
   ```

5. Run the application:

   ```bash
   uv run python src/cli/main.py
   ```

---

## Available Commands

Once the application starts, you can use the following commands:

* `add <title> [description] [--priority <level>] [--tags <tag1,tag2,...>]`
  Add a new task with optional priority and tags

* `list [--sort <field>] [--filter <type:value>] [--search <keyword>]`
  Display all tasks with optional sorting, filtering, and searching

* `update <id> [--title <title>] [--description <description>] [--priority <level>] [--tags <tag1,tag2,...>]`
  Update an existing task by ID

* `delete <id>`
  Delete a task by ID

* `complete <id>`
  Mark a task as complete

* `incomplete <id>`
  Mark a task as incomplete

* `search <keyword>`
  Search tasks by keyword

* `help`
  Display available commands

* `quit` or `exit`
  Exit the application

---

## Command Options

* `--priority <level>`
  Accepted values: `High`, `Medium`, `Low`

* `--tags <tag1,tag2,...>`
  Comma-separated list of tags

* `--sort <field>`
  Sort by `priority`, `status`, or `title`

* `--filter <type:value>`
  Examples:

  * `status:completed`
  * `priority:High`
  * `tag:work`

* `--search <keyword>`
  Search in title, description, and tags

---

## Example Usage

```text
> add "Buy groceries" "Shopping for dinner" --priority High --tags shopping,urgent
[SUCCESS] Task added with ID: 1

> add "Complete project" "Finish the todo app implementation" --priority Medium --tags work,important
[SUCCESS] Task added with ID: 2

> list
[1] 🔴 ○ Buy groceries - Shopping for dinner | Priority: High | Tags: shopping, urgent | Status: ○ Incomplete
[2] 🟡 ○ Complete project - Finish the todo app implementation | Priority: Medium | Tags: important, work | Status: ○ Incomplete

> complete 1
[SUCCESS] Task 1 marked as complete

> list --filter tag:work
[2] 🟡 ○ Complete project - Finish the todo app implementation | Priority: Medium | Tags: important, work | Status: ○ Incomplete

> quit
Goodbye!
```

---

## Error Handling

The application provides clear error messages for common issues, including:

* Unknown or invalid commands
* Non-existent task IDs
* Missing required arguments
* Title length over 100 characters
* Description length over 500 characters
* Invalid priority values
* Empty or malformed tags
* Invalid filter or sort formats

---

## Notes

* All tasks are stored in memory and reset when the application exits
* Designed for learning, demos, and CLI best practices
* Easy to extend with persistence or additional features

---

Happy task tracking 🚀
