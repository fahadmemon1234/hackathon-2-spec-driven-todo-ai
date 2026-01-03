# Data Model: Frontend Priority & Category Fields

**Feature**: Frontend Priority & Category Fields
**Date**: 2026-01-02
**Branch**: 12-frontend-priority-category

## Task Entity

### Attributes
- **id**: `number` - Unique identifier assigned when task is created
- **title**: `string` - Title of the task (required)
- **description**: `string | undefined` - Detailed description of the task (optional)
- **completed**: `boolean` - Completion status (default: false)
- **created_at**: `string` - Timestamp when task was created
- **updated_at**: `string` - Timestamp when task was last updated
- **priority**: `string` - Priority level of the task (required, values: "high", "medium", "low")
- **category**: `string | undefined` - Category of the task (optional)

### Validation Rules
- Title must be provided and not empty
- Priority must be one of "high", "medium", or "low"
- Category, if provided, must be between 1 and 50 characters
- Description, if provided, must meet existing length requirements

### State Transitions
- A task can transition from any priority level to any other priority level
- A task can transition from having no category to having a category
- A task can transition from having a category to having no category (empty)

## Relationships
- No relationships needed as this is an extension of the existing Task entity

## Operations
- Create: New task with all attributes including priority (default "medium") and optional category
- Read: Retrieve task by id with all attributes
- Update: Modify any attributes including priority and category
- Delete: Remove task by id