# Dapr Component Configurations

This document describes the Dapr components used in the Todo Application.

## 1. Pub/Sub Component (Kafka)

The pub/sub component enables event-driven communication between services using Apache Kafka.

### Configuration File: `components/pubsub.yaml`

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

### Topics Used:
- `task-events`: For task creation, updates, and deletion notifications
- `reminders`: For reminder scheduling and notifications
- `task-updates`: For task status and property changes

## 2. State Store Component (Redis)

The state store component provides persistent state management using Redis.

### Configuration File: `components/statestore.yaml`

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

### State Key Patterns:
- `task:{taskId}`: Stores individual task state
- `recurrence:{taskId}`: Stores recurrence metadata for recurring tasks
- `reminder:{reminderId}`: Stores reminder schedule information

## 3. Cron Binding Component

The cron binding component enables scheduled tasks and reminder processing.

### Configuration File: `components/cron-binding.yaml`

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

### Usage:
- Triggers scheduled reminder processing
- Invokes backend endpoints at specified intervals
- Enables recurring task processing

## 4. Secrets Component

The secrets component provides secure configuration management.

### Configuration File: `components/secrets.yaml`

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
    value: "/secrets/secrets.json"
  - name: nestedSeparator
    value: ":"
```

### Secrets Used:
- `kafka_brokers`: Kafka connection string
- `redis_host`: Redis connection string
- `redis_password`: Redis password (can be empty)

## 5. Service Invocation

Dapr automatically handles service invocation between services with the following configuration:

- App ID: `backend-service`
- HTTP Port: 3500 (default Dapr HTTP port)
- gRPC Port: 50001 (default Dapr gRPC port)

## Component Locations

All component configuration files are located in the `components/` directory at the project root. The Dapr sidecar is configured to load components from this directory.

## Component Validation

To validate component configurations:

1. Check syntax with Dapr CLI:
   ```bash
   dapr components -k
   ```

2. Verify components are loaded:
   ```bash
   dapr status -k
   ```

3. Test component functionality through the application endpoints.