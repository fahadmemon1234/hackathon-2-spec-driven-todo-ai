# Data Model for Dapr Integration

## Entities

### Task
- Fields:
  - taskId (string): Unique identifier for the task
  - title (string): Title of the task
  - description (string): Detailed description of the task
  - status (string): Current status (e.g., pending, in-progress, completed)
  - priority (string): Priority level (e.g., low, medium, high)
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

## Validation Rules

### Task
- Title is required and must be between 1-200 characters
- Status must be one of: pending, in-progress, completed
- Due date must be in the future if provided
- Priority must be one of: low, medium, high

### Reminder
- Reminder time must be in the future
- Associated task must exist
- Notified flag defaults to false

### RecurrenceMetadata
- Recurrence rule must follow standard recurrence rule format
- Next occurrence must be calculated based on recurrence rule
- End date must be after last occurrence if provided

## State Transitions

### Task Status Transitions
- pending → in-progress
- in-progress → completed
- completed → in-progress (for reopening)
- in-progress → pending (for deferring)

### Reminder Notification
- notified = false → notified = true (when reminder is sent)