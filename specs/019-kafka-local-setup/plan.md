# Kafka Local Setup - Implementation Plan

## 1. Overview & Assumptions
This plan implements a reliable local Kafka development environment using Docker Compose with a single broker and Zookeeper. The setup resolves the common Docker listener/advertised.listeners mismatch issue by configuring dual listeners for internal and external access.
- Assumptions: Docker Desktop (Win/Mac), host.docker.internal works, no existing port conflicts on 2181/9092/29092

## 2. Tech Stack
- Docker Desktop (version 20.10 or later)
- Docker Compose plugin
- bitnami/kafka:3.7 image
- bitnami/zookeeper:3.8 image
- Python 3.8+ with kafka-python library

## 3. Project Structure
```
specs/
└── 019-kafka-local-setup/
    ├── spec.md
    ├── plan.md
    └── tasks.md
```

## 4. Architecture
- Single Kafka broker with Zookeeper
- Dual listeners configuration:
  - INTERNAL: For container-to-container communication
  - EXTERNAL: For host machine access
- Advertised listeners mapping:
  - INTERNAL://kafka:9092 (for internal access)
  - EXTERNAL://localhost:9092 (for external access)

## 5. Configuration Details
- KAFKA_CFG_LISTENERS: INTERNAL://:9092,EXTERNAL://:29092
- KAFKA_CFG_ADVERTISED_LISTENERS: INTERNAL://kafka:9092,EXTERNAL://localhost:9092
- KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP: INTERNAL:PLAINTEXT,EXTERNAL:PLAINTEXT
- KAFKA_CFG_INTER_BROKER_LISTENER_NAME: INTERNAL
- KAFKA_CFG_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
- KAFKA_CFG_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1
- KAFKA_CFG_TRANSACTION_STATE_LOG_MIN_ISR: 1
- KAFKA_CFG_DEFAULT_REPLICATION_FACTOR: 1