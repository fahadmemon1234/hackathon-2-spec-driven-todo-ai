# Quickstart Guide for Dapr Integration

## Prerequisites

- Docker and Docker Compose
- Dapr CLI installed and initialized
- Python 3.8+ (for backend development)
- Node.js (for frontend, if applicable)

## Setup Instructions

### 1. Install Dapr

```bash
# Download and install Dapr CLI
# Then initialize Dapr in standalone mode
dapr init
```

### 2. Clone and Navigate to Project

```bash
# Clone the repository (if not already done)
cd todo-app-Phase-5
```

### 3. Start the Services

```bash
# Navigate to the project directory
cd F:\Programing\governor Inititative Program IT\Ai\Hackathon 2\todo-app-Phase-5

# Start all services including Dapr sidecars
docker-compose up -d
```

### 4. Verify Dapr Components

```bash
# Check if Dapr sidecars are running
dapr list
```

### 5. Run the Application

```bash
# Run the backend with Dapr sidecar
dapr run --app-id backend-service --app-port 8000 --dapr-http-port 3500 python backend/main.py
```

## Key Configuration Files

- `components/pubsub.yaml` - Kafka pub/sub configuration
- `components/statestore.yaml` - Redis state store configuration
- `components/cron-binding.yaml` - Cron binding configuration
- `components/secrets.yaml` - Secrets configuration
- `secrets.json` - Actual secrets file (not committed to repo)

## Common Commands

```bash
# View Dapr logs
dapr logs

# Publish a test message to Kafka via Dapr
curl -X POST http://localhost:3500/v1.0/publish/kafka-pubsub/task-events -H "Content-Type: application/json" -d '{"taskId": "123", "action": "created"}'

# Get state via Dapr
curl http://localhost:3500/v1.0/state/statestore/task:123

# Save state via Dapr
curl -X POST http://localhost:3500/v1.0/state/statestore -H "Content-Type: application/json" -d '[{ "key": "task:123", "value": {"title": "Test Task", "status": "pending"}}]'
```

## Troubleshooting

1. If Dapr sidecar fails to start:
   - Ensure Dapr is properly initialized: `dapr init`
   - Check that ports are not in use by other processes

2. If Kafka connection fails:
   - Verify Kafka is running: `docker ps | grep kafka`
   - Check Kafka logs: `docker logs <kafka-container-id>`

3. If Redis connection fails:
   - Verify Redis is running: `docker ps | grep redis`
   - Check Redis logs: `docker logs <redis-container-id>`

4. If component files are not loaded:
   - Verify component files are in the correct directory
   - Check that file permissions allow Dapr to read them