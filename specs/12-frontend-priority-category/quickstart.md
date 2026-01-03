# Quickstart Guide: Frontend Priority & Category Fields

**Feature**: Frontend Priority & Category Fields
**Date**: 2026-01-02
**Branch**: 12-frontend-priority-category

## Setup Instructions

1. Ensure you have Node.js 18+ installed on your system
2. Navigate to the frontend directory
3. Install project dependencies:
   ```bash
   npm install
   ```
4. Start the development server:
   ```bash
   npm run dev
   ```
5. The application will be available at `http://localhost:3000`

## Feature Usage

Once the application is running, you can use the enhanced task forms:

### Creating Tasks with Priority and Category
1. Click the "Add Task" button to open the task creation modal
2. Enter the task title and description
3. Select a priority level (High, Medium, Low) using the colored buttons
4. Optionally enter a category or select from the suggestions
5. Click "Save" to create the task

### Editing Tasks with Priority and Category
1. Click on an existing task to open the edit modal
2. The priority and category fields will be pre-filled with existing values
3. Modify the priority or category as needed
4. Click "Save" to update the task

## Available Components

The following components were updated or created:

- `TaskFormModal.tsx`: Enhanced with priority selector and category input
- `types/task.ts`: Updated Task interface with priority and category fields
- `lib/api.ts`: Updated API functions to handle priority and category

## Example Usage

```
When creating a new task:
- Title: "Complete project proposal"
- Priority: High (red button)
- Category: "work"

When editing an existing task:
- The form will pre-populate with existing values
- You can change priority from "medium" to "high"
- You can add or modify the category
```

## Testing

To run the tests for the new functionality:

```bash
npm test
```

This will run both unit and integration tests for the updated components.