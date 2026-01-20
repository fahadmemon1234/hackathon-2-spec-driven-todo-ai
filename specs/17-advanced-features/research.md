# Research Findings: Advanced Features Implementation

**Feature**: Advanced Features, Event-Driven Architecture and Cloud Deployment
**Created**: 2026-01-19

## Decision: Dapr Configuration for Minikube

**Rationale**: Dapr needs to be properly configured to work with Minikube for local testing, ensuring consistency between local development and cloud deployment.

**Approach**: Using Dapr in Kubernetes mode on Minikube to mirror the production environment as closely as possible.

**Steps**:
1. Install Dapr in Kubernetes mode on Minikube:
   ```bash
   dapr init -k
   ```
2. Verify installation:
   ```bash
   dapr status -k
   ```
3. Configure Dapr components for pub/sub, secrets, and bindings.

**Benefits**:
- Consistency between local and cloud environments
- Proper isolation of services
- Realistic testing of distributed system behavior

## Decision: Redpanda for Local Development

**Rationale**: Need to choose between Kafka and Redpanda for local development, considering resource usage and ease of setup.

**Approach**: Using Redpanda for local development due to its lighter resource requirements while maintaining Kafka API compatibility.

**Configuration**:
1. Deploy Redpanda to Minikube:
   ```bash
   kubectl create namespace redpanda
   helm repo add redpanda https://charts.redpanda.com
   helm repo update
   helm install redpanda redpanda/redpanda --namespace redpanda
   ```
2. Verify deployment:
   ```bash
   kubectl get pods -n redpanda
   ```

**Benefits**:
- Lower resource consumption than Kafka
- Full Kafka API compatibility
- Faster startup times for local development
- Simplified configuration

## Decision: dateutil.rrule for Recurrence Rule Parsing

**Rationale**: Need a reliable library to calculate next occurrence dates based on recurrence rules that follows established standards.

**Approach**: Using dateutil.rrule which implements the iCalendar recurrence rules (RFC 5545).

**Implementation**:
```python
from dateutil.rrule import rrulestr
from datetime import datetime, timedelta

def calculate_next_occurrence(recurrence_rule: str, start_date: datetime) -> datetime:
    """
    Calculate the next occurrence based on the recurrence rule.
    recurrence_rule format: "FREQ=DAILY", "FREQ=WEEKLY;BYDAY=MO,WE", etc.
    """
    try:
        rule = rrulestr(recurrence_rule, dtstart=start_date)
        next_occurrence = next(rule.after(start_date))
        return next_occurrence
    except Exception as e:
        raise ValueError(f"Invalid recurrence rule: {e}")
```

**Benefits**:
- Robust implementation of iCalendar standards
- Handles complex recurrence patterns
- Well-tested and maintained library
- Supports all required recurrence types (daily, weekly, monthly, yearly)

## Decision: JSON Column for Tag Storage

**Rationale**: Need to store and index tags for efficient querying while maintaining flexibility.

**Approach**: Using PostgreSQL's JSON column type with GIN indexing for efficient tag-based queries.

**Schema**:
```sql
ALTER TABLE task ADD COLUMN tags JSON;
CREATE INDEX idx_task_tags ON task USING GIN (tags);
```

**Querying**:
```sql
-- Find tasks with specific tag
SELECT * FROM task WHERE tags ? 'work';

-- Find tasks with any of multiple tags
SELECT * FROM task WHERE tags ?| ARRAY['work', 'personal'];

-- Find tasks with all of multiple tags
SELECT * FROM task WHERE tags ?& ARRAY['work', 'urgent'];
```

**Benefits**:
- Flexible storage for variable number of tags
- Efficient querying with GIN index
- Native PostgreSQL support
- Easy to modify tag structure if needed

## Additional Research: Timezone Handling

**Rationale**: Need to properly handle timezone differences for due dates and reminders to ensure accurate scheduling.

**Approach**: Store all datetime values in UTC in the database and convert to user's local timezone in the frontend.

**Implementation**:
1. Store all datetime values in UTC in the database
2. Include user's timezone in user profile
3. Convert to user's timezone when displaying due dates
4. Convert from user's timezone to UTC when storing due dates

**Benefits**:
- Consistent storage regardless of user location
- Accurate scheduling across different timezones
- Proper handling of daylight saving time changes

## Additional Research: Reminder Scheduling Strategy

**Rationale**: Need to determine the best approach for scheduling and triggering reminders.

**Approach**: Two-part system:
1. Event-based: When a task with a due date is created/updated, publish a reminder event with the scheduled reminder time
2. Polling-based: A service periodically checks for upcoming reminders and triggers notifications

**Implementation**:
1. When creating/updating a task with due_date, calculate remind_at (e.g., due_date - 1 hour) and publish to reminders topic
2. Notification service consumes these events and stores them in a scheduled reminders queue
3. A cron binding or periodic service checks for reminders that should be sent now

**Benefits**:
- Decouples reminder scheduling from task creation
- Allows for flexible reminder timing (e.g., 1 hour before, 1 day before)
- Resilient to service restarts (reminders are persisted)

## Additional Research: Error Handling and Retry Logic

**Rationale**: Need to implement proper error handling and retry mechanisms for the event-driven architecture.

**Approach**: Implement dead letter queues and retry policies using Dapr's built-in capabilities.

**Implementation**:
1. Configure Dapr pub/sub components with retry policies
2. Implement dead letter queues for failed message processing
3. Add circuit breaker patterns for service invocations

**Benefits**:
- Improved system resilience
- Better fault tolerance
- Automatic recovery from transient failures