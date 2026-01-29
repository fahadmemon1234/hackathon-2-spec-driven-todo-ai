# Data Model for Minikube Deployment

## Overview

The data model for the Minikube deployment remains identical to the Docker Compose implementation. The Kubernetes deployment is an infrastructure change that doesn't alter the application's data structures or relationships.

## Entities

### Task
- Fields:
  - taskId (string): Unique identifier for the task
  - title (string): Title of the task
  - description (string): Detailed description of the task
  - status (string): Current status (pending, in-progress, completed)
  - priority (string): Priority level (low, medium, high)
  - createdAt (datetime): Timestamp when task was created
  - updatedAt (datetime): Timestamp when task was last updated
  - dueDate (datetime): Due date for the task
  - recurrenceRule (string): Rule for recurring tasks (if applicable)

### Reminder
- Fields:
  - reminderId (string): Unique identifier for the reminder
  - taskId (string): Reference to the associated task
  - reminderTime (datetime): Time when reminder should be triggered
  - notified (boolean): Flag indicating if reminder has been sent
  - createdAt (datetime): Timestamp when reminder was created

### RecurrenceMetadata
- Fields:
  - taskId (string): Reference to the associated task
  - recurrenceRule (string): Rule defining recurrence pattern
  - lastOccurrence (datetime): Time of last occurrence
  - nextOccurrence (datetime): Time of next occurrence
  - endDate (datetime): End date for recurrence (optional)

## State Key Patterns

### Task State
- Key: `task:{taskId}`
- Value: Serialized Task object

### Recurrence Metadata
- Key: `recurrence:{taskId}`
- Value: Serialized RecurrenceMetadata object

### Reminder Schedule
- Key: `reminder:{reminderId}`
- Value: Serialized Reminder object

## Kubernetes-Specific Considerations

### Configuration Management
- Use Kubernetes ConfigMaps for non-sensitive configuration
- Use Kubernetes Secrets for sensitive configuration (passwords, tokens)
- Dapr components will be deployed as Kubernetes CRDs (Custom Resource Definitions)

### Persistent Storage
- PostgreSQL data stored in PersistentVolumeClaim
- Redis data stored in PersistentVolumeClaim (if persistence required)
- Dapr state store data managed by Dapr runtime with configured storage

### Service Discovery
- Internal service communication uses Kubernetes DNS: `<service-name>.<namespace>.svc.cluster.local`
- Dapr sidecars use service names for service invocation
- Kafka and Redis accessed via Kubernetes service names

## Validation Rules

Same as the original data model:
- Task title is required and must be between 1-200 characters
- Task status must be one of: pending, in-progress, completed
- Due date must be in the future if provided
- Priority must be one of: low, medium, high
- Reminder time must be in the future
- Recurrence rule must follow standard recurrence rule format