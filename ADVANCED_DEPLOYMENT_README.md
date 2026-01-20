# Advanced Cloud Deployment: Todo App with Kafka and Dapr

This project implements an advanced todo application with event-driven architecture using Kafka and Dapr, deployed on Kubernetes.

## Architecture Overview

The system consists of the following components:

- **Frontend Service**: Next.js application for user interface
- **Backend API**: FastAPI application handling business logic
- **Notification Service**: Handles reminder notifications
- **Recurring Task Service**: Manages recurring tasks
- **WebSocket Service**: Provides real-time updates
- **Kafka Cluster**: Event streaming platform
- **Dapr**: Distributed application runtime for pub/sub, state management, etc.

## Event-Driven Architecture

The application uses Kafka for event-driven communication between services:

1. **Task Events**: All task operations (create, update, delete, complete) are published to the `task-events` topic
2. **Reminders**: Tasks with due dates trigger reminder events published to the `reminders` topic
3. **Real-time Updates**: Task changes are broadcast to the `task-updates` topic for real-time client synchronization

## Dapr Integration

Dapr provides the following building blocks:

- **Pub/Sub**: Abstraction over Kafka for event publishing/subscribing
- **State Management**: For storing application state
- **Service Invocation**: For inter-service communication
- **Bindings**: For connecting to external systems
- **Secrets Management**: For secure credential storage

## Deployment Options

### Local Deployment with Minikube

1. Install prerequisites:
   - Minikube
   - kubectl
   - Helm
   - Dapr CLI

2. Start Minikube:
   ```bash
   minikube start
   ```

3. Install Dapr:
   ```bash
   dapr init -k
   ```

4. Deploy Kafka using Strimzi:
   ```bash
   kubectl create namespace kafka
   kubectl apply -f https://strimzi.io/install/latest?namespace=kafka
   kubectl apply -f k8s/base/kafka-cluster.yaml
   ```

5. Deploy the application:
   ```bash
   kubectl apply -k k8s/minikube/
   ```

### Cloud Deployment (AKS/GKE)

The application can be deployed to cloud Kubernetes services like Azure AKS or Google GKE using the provided Helm chart.

## Services

### Backend Service
Handles all task-related operations and publishes events to Kafka via Dapr.

### Notification Service
Consumes reminder events from Kafka and sends notifications to users.

### Recurring Task Service
Consumes task completion events and creates new instances of recurring tasks.

### WebSocket Service
Consumes task update events and broadcasts them to connected clients for real-time synchronization.

## Kafka Topics

- `task-events`: All task CRUD operations
- `reminders`: Scheduled reminder triggers  
- `task-updates`: Real-time client sync

## Dapr Components

- `kafka-pubsub`: Kafka pub/sub component
- `statestore`: State management component
- `secrets-store`: Secrets management component

## CI/CD Pipeline

The project includes a GitHub Actions workflow that:
1. Runs tests and linting
2. Builds Docker images for all services
3. Deploys to Minikube for development
4. Deploys to AKS for production

## Monitoring and Logging

The deployment includes:
- Prometheus for metrics collection
- Grafana for visualization
- Centralized logging setup
- Alerts configuration

## Advanced Features

- Recurring tasks with RRULE support
- Due dates and reminders
- Priorities, tags, search, filter, sort
- Real-time synchronization across clients
- Event-driven architecture for scalability
- Dapr for simplified microservice development