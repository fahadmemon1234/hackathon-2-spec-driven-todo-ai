# Todo Application – Dapr Integration (Local Docker Compose) Specification

## 1. Overview

This specification outlines the implementation of Dapr (Distributed Application Runtime) for the Todo Application backend using Docker Compose. The goal is to leverage Dapr's building blocks to enhance the application's capabilities with pub/sub messaging, state management, cron bindings, secrets management, and service invocation - all running locally without Kubernetes or cloud infrastructure.

Current Status:
- Kafka is running locally via Docker (topics healthy)
- Backend service is running (HTTP port 8000)
- No Dapr sidecars or components implemented yet

## 2. Architecture Diagram (text-based)

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Dapr Sidecar   │    │   Backend       │
│                 │◄──►│  (App ID:       │◄──►│                 │
│                 │    │  backend-service)│    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │   Dapr Runtime   │
                    │                  │
                    └──────────────────┘
                              │
            ┌─────────────────┼─────────────────┐
            ▼                 ▼                 ▼
    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
    │ Kafka        │  │ Redis        │  │ Secrets      │
    │ (Pub/Sub)    │  │ (State Store)│  │ (Secrets)    │
    └──────────────┘  └──────────────┘  └──────────────┘
```

## 3. Components List

- Dapr Sidecar: Runs alongside the backend service
- App ID: backend-service
- Dapr Components:
  - kafka-pubsub: For pub/sub messaging
  - statestore: For state persistence
  - cron-binding: For scheduled tasks
  - secrets: For secure configuration

## 4. Docker Compose Integration

The Docker Compose setup will include:
- Backend service container
- Dapr sidecar container (daprd)
- Kafka cluster containers
- Redis container for state storage
- Configuration files for Dapr components

Dapr sidecar will be injected into the backend service container or run as a separate container linked to the backend.

## 5. Dapr Components Specification

### 5.1 Pub/Sub Component

Component name: kafka-pubsub
Message broker: Apache Kafka
Topics:
- task-events: For task creation, updates, and deletion notifications
- reminders: For reminder scheduling and notifications
- task-updates: For task status and property changes

Configuration:
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: "kafka:9092"
  - name: consumerGroup
    value: "backend-service-consumer"
  - name: authRequired
    value: "false"
```

Backend publishing to topics using Dapr HTTP API:
- POST to `http://localhost:3500/v1.0/publish/kafka-pubsub/<topic-name>`

Backend subscribing to topics using Dapr HTTP API:
- Dapr will invoke backend endpoints based on subscription configuration

### 5.2 State Store Component

Component name: statestore
Data store: Redis
Use cases:
- Store task state
- Store recurrence metadata
- Store reminder schedules

Configuration:
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
spec:
  type: state.redis
  version: v1
  metadata:
  - name: redisHost
    value: "redis:6379"
  - name: redisPassword
    value: ""
  - name: actorStateStore
    value: "true"
```

Example state key structure:
- `task:{taskId}`: Stores individual task state
- `recurrence:{taskId}`: Stores recurrence metadata for recurring tasks
- `reminder:{reminderId}`: Stores reminder schedule information

Operations using Dapr HTTP API:
- GET `http://localhost:3500/v1.0/state/statestore/{key}`: Retrieve state
- POST `http://localhost:3500/v1.0/state/statestore`: Save state
- DELETE `http://localhost:3500/v1.0/state/statestore/{key}`: Delete state

### 5.3 Cron Binding Component

Component name: cron-binding
Trigger: Scheduled reminder events
Integration: Publishes events to Kafka using pub/sub

Configuration:
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: reminder-cron
spec:
  type: bindings.cron
  version: v1
  metadata:
  - name: schedule
    value: "*/5 * * * *"  # Every 5 minutes for testing
```

Flow:
1. Cron binding triggers at scheduled intervals
2. Dapr invokes backend endpoint to process scheduled reminders
3. Backend publishes reminder events to Kafka using pub/sub component

### 5.4 Secrets Component

Component name: secrets
Abstraction: Secret management for configuration
Protected values:
- Kafka brokers connection string
- Redis host and password

Configuration:
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: local-secret-store
spec:
  type: secretstores.local.file
  version: v1
  metadata:
  - name: secretsFile
    value: "/path/to/secrets.json"
  - name: nestedSeparator
    value: ":"
```

Secrets file structure (secrets.json):
```json
{
  "kafka_brokers": "kafka:9092",
  "redis_host": "redis:6379",
  "redis_password": ""
}
```

Backend reads secrets via Dapr HTTP API:
- GET `http://localhost:3500/v1.0/secrets/local-secret-store/{secret-key}`

## 6. Backend Integration Flow

1. Backend service starts with Dapr sidecar
2. Dapr sidecar loads component configurations
3. Backend uses Dapr HTTP APIs for all Dapr operations:
   - Publishing messages to Kafka via pub/sub
   - Storing/retrieving state in Redis
   - Reading secrets from secret store
   - Invoking other services via service invocation
4. Cron binding triggers scheduled operations
5. Subscriptions receive messages from Kafka topics

## 7. Event Flow Examples

### 7.1 Task Creation Flow
1. Frontend sends task creation request to backend
2. Backend stores task in state store via Dapr API
3. Backend publishes "task-created" event to "task-events" topic via Dapr API
4. Other services consume the event from Kafka

### 7.2 Reminder Scheduling Flow
1. Backend stores reminder schedule in state store via Dapr API
2. Cron binding triggers at scheduled interval
3. Dapr invokes backend endpoint to process scheduled reminders
4. Backend publishes reminder notification to "reminders" topic via Dapr API

### 7.3 Recurring Task Processing Flow
1. Backend stores recurrence metadata in state store via Dapr API
2. Cron binding triggers at scheduled interval
3. Backend retrieves recurrence metadata from state store
4. Backend creates new task instance based on recurrence rules
5. Backend publishes "task-created" event to "task-events" topic

## 8. Local Development Notes

- Dapr runtime must be installed locally (dapr init)
- Docker Compose should start all services including Dapr sidecars
- Use dapr run command to run services with Dapr sidecar during development
- Component files should be placed in ./components directory
- Environment variables for local development should be documented
- Port bindings for Dapr API (default 3500) should not conflict with other services

## 9. Verification Checklist

- [ ] Dapr sidecar successfully connects to backend service
- [ ] Pub/Sub component connects to Kafka and can publish/subscribe messages
- [ ] State store component connects to Redis and can store/retrieve data
- [ ] Cron binding triggers at specified intervals
- [ ] Secrets component loads and provides secret values to backend
- [ ] Service invocation works between backend services
- [ ] All Dapr HTTP API calls return expected responses
- [ ] Docker Compose starts all services without errors
- [ ] Task creation/deletion triggers appropriate events
- [ ] Reminder scheduling and notifications work as expected
- [ ] Recurring task processing executes correctly
- [ ] Error handling works when Dapr components are unavailable