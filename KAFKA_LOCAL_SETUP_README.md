# Kafka Local Development Setup

This setup provides a local Kafka environment using Docker Compose with a single broker and Zookeeper. It resolves the common Docker listener/advertised.listeners mismatch issue by configuring dual listeners for internal and external access.

## Prerequisites

- Docker Desktop (version 20.10 or later)
- Docker Compose plugin enabled
- Python 3.8+ with pip (for connectivity testing)

## Setup Instructions

1. Clone or download this repository
2. Navigate to the project directory
3. Start the Kafka stack using Docker Compose:

```bash
docker-compose -f docker-compose.kafka.yml up -d
```

## Available Services

- Zookeeper: Running on port 2181
- Kafka:
  - Internal access: kafka:9092 (within Docker network)
  - External access: localhost:29092 (from host machine)

## Pre-configured Topics

The following topics need to be created manually after startup:
- `task-events`: 3 partitions, 1 replica
- `reminders`: 1 partition, 1 replica
- `task-updates`: 3 partitions, 1 replica

To create these topics:

```bash
# Create task-events topic
docker-compose -f docker-compose.kafka.yml exec kafka kafka-topics \
  --create \
  --topic task-events \
  --bootstrap-server localhost:29092 \
  --partitions 3 \
  --replication-factor 1

# Create reminders topic
docker-compose -f docker-compose.kafka.yml exec kafka kafka-topics \
  --create \
  --topic reminders \
  --bootstrap-server localhost:29092 \
  --partitions 1 \
  --replication-factor 1

# Create task-updates topic
docker-compose -f docker-compose.kafka.yml exec kafka kafka-topics \
  --create \
  --topic task-updates \
  --bootstrap-server localhost:29092 \
  --partitions 3 \
  --replication-factor 1
```

## Testing Connectivity

To test connectivity from your host machine, you can use the provided Python script:

```bash
python test_connectivity.py
```

Or manually test with any Kafka client connecting to `localhost:29092`.

## Managing Topics

To create additional topics, use the Kafka CLI:

```bash
docker-compose -f docker-compose.kafka.yml exec kafka kafka-topics \
  --create \
  --topic your-topic-name \
  --bootstrap-server localhost:29092 \
  --partitions 3 \
  --replication-factor 1
```

## Stopping the Services

To stop the Kafka and Zookeeper services:

```bash
docker-compose -f docker-compose.kafka.yml down
```

## Troubleshooting

### Common Issues

1. **Connection timeouts**: Make sure the Kafka container is fully started before connecting. Check logs with `docker-compose -f docker-compose.kafka.yml logs kafka`.

2. **Listener configuration**: The setup uses dual listeners:
   - PLAINTEXT://kafka:9092 for container-to-container communication
   - PLAINTEXT_HOST://host.docker.internal:29092 for host access

3. **Zookeeper connection issues**: The configuration includes health checks to ensure Zookeeper is ready before Kafka starts.

4. **Port conflicts**: Ensure ports 2181, 9092, and 29092 are available on your host machine.

### Verifying Setup

To verify all topics exist with correct settings:

```bash
docker-compose -f docker-compose.kafka.yml exec kafka kafka-topics \
  --describe \
  --bootstrap-server localhost:29092
```

## Configuration Details

The Kafka setup uses the following important configurations:
- Single broker setup with replication factor = 1 for all topics
- Offsets topic replication factor = 1
- Transaction state log replication factor = 1
- Auto topic creation enabled
- Dual listeners for internal and external access
- Health checks to ensure Zookeeper is ready before Kafka starts