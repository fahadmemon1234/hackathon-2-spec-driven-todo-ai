# Todo CLI App

A command-line todo application that manages tasks in memory, demonstrating core CRUD operations plus task completion and advanced organization features.

## Features

- Add new tasks with title, description, priority, and tags
- View all tasks with status indicators, priority levels, and tags
- Mark tasks as complete/incomplete
- Update task details, priority, and tags
- Delete tasks
- Search tasks by keyword in title, description, or tags
- Filter tasks by status, priority, or tag
- Sort tasks by priority, status, or title
- Comprehensive error handling and validation

## Setup Instructions

1. Ensure you have Python 3.13+ installed on your system
2. Install UV package manager if not already installed:
   ```bash
   pip install uv
   ```
3. Navigate to the project root directory
4. Install project dependencies:
   ```bash
   uv sync
   ```
5. Run the application:
   ```bash
   uv run python src/cli/main.py
   ```

## Available Commands

Once the application is running, you can use the following commands:

- `add <title> [description] [--priority <level>] [--tags <tag1,tag2,...>]` - Add a new task with optional priority and tags
- `list [--sort <field>] [--filter <type:value>] [--search <keyword>]` - Display all tasks with optional sorting, filtering, and searching
- `update <id> [--title <title>] [--description <description>] [--priority <level>] [--tags <tag1,tag2,...>]` - Update task details by ID
- `delete <id>` - Delete a task by ID
- `complete <id>` - Mark a task as complete by ID
- `incomplete <id>` - Mark a task as incomplete by ID
- `search <keyword>` - Search tasks by keyword in title, description, or tags
- `help` - Show available commands
- `quit` or `exit` - Exit the application

## Command Options

- `--priority <level>` - Priority level (High, Medium, Low)
- `--tags <tag1,tag2,...>` - Comma-separated list of tags
- `--sort <field>` - Sort by field (priority, status, title)
- `--filter <type:value>` - Filter by type and value (status:completed, priority:High, tag:work)
- `--search <keyword>` - Search by keyword in title, description, or tags

## Example Usage

```
> add "Buy groceries" "Shopping for dinner" --priority High --tags shopping,urgent
[SUCCESS] Task added with ID: 1 | Title: Buy groceries | Priority: High | Tags: {'shopping', 'urgent'}

> add "Complete project" "Finish the todo app implementation" --priority Medium --tags work,important
[SUCCESS] Task added with ID: 2 | Title: Complete project | Priority: Medium | Tags: {'work', 'important'}

> list
[1] 🔴 ○ Buy groceries - Shopping for dinner | Priority: High | Tags: shopping, urgent | Status: ○ Incomplete
[2] 🟡 ○ Complete project - Finish the todo app implementation | Priority: Medium | Tags: important, work | Status: ○ Incomplete

> complete 1
[SUCCESS] Task 1 marked as complete

> list --sort priority
[1] 🔴 ✓ Buy groceries - Shopping for dinner | Priority: High | Tags: shopping, urgent | Status: ✓ Complete
[2] 🟡 ○ Complete project - Finish the todo app implementation | Priority: Medium | Tags: important, work | Status: ○ Incomplete

> list --filter tag:work
[2] 🟡 ○ Complete project - Finish the todo app implementation | Priority: Medium | Tags: important, work | Status: ○ Incomplete

> search "project"
[SUCCESS] Found 1 task(s) containing 'project':
[2] 🟡 ○ Complete project - Finish the todo app implementation | Priority: Medium | Tags: important, work | Status: ○ Incomplete

> update 2 --priority High --tags work,important,urgent
[SUCCESS] Task 2 updated successfully

> list --filter priority:High
[1] 🔴 ✓ Buy groceries - Shopping for dinner | Priority: High | Tags: shopping, urgent | Status: ✓ Complete
[2] 🔴 ○ Complete project - Finish the todo app implementation | Priority: High | Tags: important, urgent, work | Status: ○ Incomplete

> quit
Goodbye!
```

## Error Handling

The application will display helpful error messages if:
- Invalid command is entered
- Non-existent task ID is provided
- Required parameters are missing
- Input exceeds character limits (100 chars for title, 500 for description)
- Invalid priority level is provided (must be High, Medium, or Low)
- Invalid tag format is provided (must be non-empty strings)
- Invalid filter format is used