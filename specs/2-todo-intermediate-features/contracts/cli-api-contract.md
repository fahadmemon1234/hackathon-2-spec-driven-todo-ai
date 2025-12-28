# CLI API Contracts: Todo App Intermediate Features

## Command Structure

All commands follow the pattern:
```
command [arguments] [options]
```

## Commands

### 1. Add Task
**Command**: `add`
**Description**: Add a new task with optional priority and tags
**Usage**: `add <title> [--priority <level>] [--tags <tag1,tag2,...>]`
**Arguments**:
- `title`: Task title (required)
**Options**:
- `--priority`: Priority level (High, Medium, Low)
- `--tags`: Comma-separated list of tags
**Example**: `add "Buy groceries" --priority High --tags shopping,urgent`

### 2. List Tasks
**Command**: `list`
**Description**: List all tasks with optional sorting, filtering, and searching
**Usage**: `list [--sort <field>] [--filter <type:value>] [--search <keyword>]`
**Options**:
- `--sort`: Sort by field (priority, title, status)
- `--filter`: Filter by type and value (status:completed, priority:High, tag:work)
- `--search`: Search keyword in title, description, or tags
**Examples**:
- `list`
- `list --sort priority`
- `list --filter status:completed`
- `list --filter tag:work`
- `list --search "project"`

### 3. Update Task
**Command**: `update`
**Description**: Update an existing task's priority and tags
**Usage**: `update <id> [--priority <level>] [--tags <tag1,tag2,...>]`
**Arguments**:
- `id`: Task ID (required)
**Options**:
- `--priority`: Priority level (High, Medium, Low)
- `--tags`: Comma-separated list of tags
**Example**: `update 1 --priority Medium --tags work,important`

### 4. Search Tasks
**Command**: `search`
**Description**: Search for tasks containing a keyword
**Usage**: `search <keyword>`
**Arguments**:
- `keyword`: Search term (required)
**Example**: `search "grocery"`

### 5. Mark Task Complete
**Command**: `complete`
**Description**: Mark a task as complete
**Usage**: `complete <id>`
**Arguments**:
- `id`: Task ID (required)
**Example**: `complete 1`

### 6. Mark Task Incomplete
**Command**: `incomplete`
**Description**: Mark a task as incomplete
**Usage**: `incomplete <id>`
**Arguments**:
- `id`: Task ID (required)
**Example**: `incomplete 1`

### 7. Delete Task
**Command**: `delete`
**Description**: Delete a task
**Usage**: `delete <id>`
**Arguments**:
- `id`: Task ID (required)
**Example**: `delete 1`

### 8. Help
**Command**: `help`
**Description**: Show available commands or help for a specific command
**Usage**: `help [command]`
**Arguments**:
- `command`: Optional command name for specific help
**Examples**:
- `help`
- `help add`

## Response Format

### Success Response
```
[SUCCESS] <message>
```

### Error Response
```
[ERROR] <error message>
```

### Task Display Format
```
[ID] [TITLE] - [DESCRIPTION] | Priority: [PRIORITY] | Tags: [TAGS] | Status: [STATUS]
```

### Example Task Display
```
[1] Buy groceries - Weekly shopping | Priority: High | Tags: shopping,urgent | Status: Incomplete
```

## Validation Rules

### Priority Validation
- Must be one of: "High", "Medium", "Low"
- Case-sensitive
- Required if provided

### Tag Validation
- Must be non-empty strings
- Multiple tags separated by commas
- No duplicate tags per task

### ID Validation
- Must be a positive integer
- Must exist in the task list

### Search Validation
- Keyword must be at least 1 character
- Search is case-insensitive