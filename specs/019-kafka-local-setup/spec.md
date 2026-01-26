# Kafka Local Development Setup - Software Specification

## Feature Overview
Set up a reliable local Kafka development environment using Docker Compose with a single broker and Zookeeper. The setup resolves the common Docker listener/advertised.listeners mismatch issue by configuring dual listeners for internal and external access.

## User Stories
- **US1**: As a developer, I want to start a Kafka stack locally so that I can develop event-driven applications without external dependencies.
- **US2**: As a developer, I want to create predefined topics automatically so that I can focus on application logic rather than infrastructure setup.
- **US3**: As a developer, I want to test Kafka connectivity from my host machine so that I can verify the setup works correctly.

## Functional Requirements
1. Kafka must be accessible from inside Docker network (other services use kafka:9092)
2. Kafka must be accessible from host machine (localhost:9092)
3. No listener mismatch or "Connection to node" errors in Kafka logs
4. Single broker setup with replication factor = 1 for offsets, transactions, etc.
5. Create these topics automatically: task-events (3 partitions, 1 replica), reminders (1 partition, 1 replica), task-updates (3 partitions, 1 replica)
6. Kafka + Zookeeper must start reliably with docker-compose up -d

## Non-Functional Requirements
- Use stable, recommended images (bitnami/kafka:3.7 or latest stable)
- Ports: Zookeeper: 2181 (internal only), Kafka: 9092 (internal), 29092 (external)
- Use host.docker.internal for external advertised listener
- Environment variables must follow Kafka 3.x naming (KAFKA_CFG_... for Bitnami)
- Minimal resource usage for local dev

## Success Criteria
- Kafka logs show "started (kafka.server.KafkaServer)" with no listener errors
- All three topics exist with correct partition and replication settings
- Python connectivity test passes (message produced and consumed successfully)
- No ERROR or FATAL messages in Kafka logs related to listeners or connections