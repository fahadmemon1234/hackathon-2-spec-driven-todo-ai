# Data Model for Recurring Tasks Feature

## Updated Task Entity

### Fields
- **id**: int (Primary Key, Auto-increment)
- **title**: str (Required, Task title)
- **description**: str | None (Optional, Task description)
- **due_date**: datetime | None (Optional, Due date/time for the task)
- **urgency**: str (Default: "MEDIUM", Values: "LOW"/"MEDIUM"/"HIGH")
- **tags**: list[str] (Optional, Array of tag strings)
- **status**: str (Default: "pending", Values: "pending"/"in_progress"/"completed")
- **user_id**: int (Foreign Key, References user who owns the task)

### New Recurrence Fields
- **recurrence_rule**: str | None (RRULE string, e.g. "FREQ=DAILY;INTERVAL=1", defines the recurrence pattern)
- **recurrence_end_date**: datetime | None (Optional, specifies when recurrence should end)
- **recurrence_max_count**: int | None (Optional, maximum number of occurrences to create)
- **original_task_id**: int | None (Foreign Key, references the original task in a recurrence series)
- **occurrence_number**: int (Default: 1, sequence number in the recurrence series - 1 for original, 2 for first repeat, etc.)

### Relationships
- A recurring task belongs to an original task via `original_task_id` foreign key
- An original task can have multiple recurring instances (children tasks)

### Validation Rules
- If `recurrence_rule` is set, the task is treated as a recurring task template
- If `original_task_id` is set, the task is an instance of a recurring series
- `occurrence_number` must be >= 1
- `recurrence_max_count` must be >= 1 if set
- `recurrence_end_date` must be in the future if set

### State Transitions
- When a recurring task (where `recurrence_rule` is set) is marked as completed:
  1. The current task status changes to "completed"
  2. A new task is created with:
     - Same title, description, urgency, tags, user_id
     - Updated due_date based on recurrence_rule
     - original_task_id pointing to the completed task's id
     - occurrence_number incremented by 1
     - status set to "pending"