# Data Model: Todo App Intermediate Features

## Updated Task Entity

### Task
Represents a todo item with title, description, completion status, priority level, and tags.

**Fields**:
- `id: int` - Unique identifier for the task
- `title: str` - Title of the task
- `description: str` - Optional description of the task
- `completed: bool` - Completion status of the task (True if completed, False otherwise)
- `priority: str` - Priority level of the task ("High", "Medium", or "Low")
- `tags: set[str]` - Collection of tags associated with the task

**Validation Rules**:
- `id` must be a positive integer
- `title` must be a non-empty string
- `priority` must be one of: "High", "Medium", "Low"
- `tags` must be a set of non-empty strings

**State Transitions**:
- `completed` can transition from False to True (mark as complete)
- `completed` can transition from True to False (mark as incomplete)

## Priority Enum

### Priority
Represents the priority levels available for tasks.

**Values**:
- `HIGH = "High"`
- `MEDIUM = "Medium"`
- `LOW = "Low"`

## Constants

### Priority Constants
```python
PRIORITY_HIGH = "High"
PRIORITY_MEDIUM = "Medium"
PRIORITY_LOW = "Low"
```

### Valid Priorities
```python
VALID_PRIORITIES = {PRIORITY_HIGH, PRIORITY_MEDIUM, PRIORITY_LOW}
```

## Relationships

### Task to Tags
- One Task can have multiple Tags (many-to-many relationship)
- Each Tag can be associated with multiple Tasks
- Tags are stored as a set within each Task object