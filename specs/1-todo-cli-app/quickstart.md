# Quickstart Guide: Todo CLI App

**Feature**: Todo CLI App
**Date**: 2025-12-27
**Branch**: 1-todo-cli-app

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

- `add <title> <description>` - Add a new task with the given title and description
- `list` - Display all tasks with their ID, title, description, and completion status
- `update <id> <title> <description>` - Update the title and description of a task by ID
- `delete <id>` - Delete a task by ID
- `complete <id>` - Mark a task as complete by ID
- `incomplete <id>` - Mark a task as incomplete by ID
- `help` - Show available commands
- `quit` or `exit` - Exit the application

## Example Usage

```
> add Buy groceries Shopping for dinner
Task added with ID: 1

> add Complete project Finish the todo app implementation
Task added with ID: 2

> list
ID: 1 | Title: Buy groceries | Description: Shopping for dinner | Status: Incomplete
ID: 2 | Title: Complete project | Description: Finish the todo app implementation | Status: Incomplete

> complete 1
Task 1 marked as complete

> list
ID: 1 | Title: Buy groceries | Description: Shopping for dinner | Status: Complete
ID: 2 | Title: Complete project | Description: Finish the todo app implementation | Status: Incomplete

> quit
Goodbye!
```

## Error Handling

The application will display helpful error messages if:
- Invalid command is entered
- Non-existent task ID is provided
- Required parameters are missing
- Input exceeds character limits (100 chars for title, 500 for description)