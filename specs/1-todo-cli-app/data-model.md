# Data Model: Todo CLI App

**Feature**: Todo CLI App
**Date**: 2025-12-27
**Branch**: 1-todo-cli-app

## Task Entity

### Attributes
- **id**: `int` - Unique identifier assigned when task is created
- **title**: `str` - Title of the task (required, max 100 characters)
- **description**: `str` - Detailed description of the task (optional, max 500 characters)
- **completed**: `bool` - Completion status (default: False)

### Validation Rules
- Title must be between 1 and 100 characters
- Description, if provided, must be between 1 and 500 characters
- ID must be a positive integer
- Completed status must be a boolean value

### State Transitions
- A task can transition from `completed=False` to `completed=True` (mark complete)
- A task can transition from `completed=True` to `completed=False` (mark incomplete)

## Relationships
- No relationships needed as this is a single entity system

## Operations
- Create: New task with id, title, description, and completed=False
- Read: Retrieve task by id
- Update: Modify title, description, or completion status by id
- Delete: Remove task by id