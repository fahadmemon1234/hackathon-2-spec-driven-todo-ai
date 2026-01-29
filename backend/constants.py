"""
Constants module for the Todo Application backend
"""

# Dapr configuration constants
DAPR_HTTP_PORT = 3500
DAPR_GRPC_PORT = 50001
DAPR_APP_ID = "backend-service"
DAPR_PUBSUB_NAME = "kafka-pubsub"
DAPR_STATE_STORE_NAME = "statestore"

# Component paths
DAPR_COMPONENTS_PATH = "./components"

# Timeout configurations
DAPR_HTTP_TIMEOUT_SECONDS = 30

# Logging configuration for Dapr
DAPR_LOG_LEVEL = "info"

# State key patterns
TASK_STATE_KEY_PATTERN = "task:{taskId}"
RECURRENCE_METADATA_KEY_PATTERN = "recurrence:{taskId}"
REMINDER_SCHEDULE_KEY_PATTERN = "reminder:{reminderId}"

# Kafka topics
TASK_EVENTS_TOPIC = "task-events"
REMINDERS_TOPIC = "reminders"
TASK_UPDATES_TOPIC = "task-updates"

# Status values
TASK_STATUS_PENDING = "pending"
TASK_STATUS_IN_PROGRESS = "in-progress"
TASK_STATUS_COMPLETED = "completed"

# Priority values
TASK_PRIORITY_LOW = "low"
TASK_PRIORITY_MEDIUM = "medium"
TASK_PRIORITY_HIGH = "high"