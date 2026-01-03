# Quickstart Guide: TaskCard Priority & Category Visual Display

**Feature**: TaskCard Priority & Category Visual Display
**Date**: 2026-01-02
**Branch**: 13-taskcard-priority-category

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

Once the application is running, you can see the enhanced TaskCard with priority and category visual displays:

### Viewing Tasks with Priority and Category
1. Navigate to the tasks page
2. Each task card will display:
   - A colored left stripe indicating priority (Red for High, Gold for Medium, Gray for Low)
   - A priority badge with uppercase text (HIGH/MEDIUM/LOW)
   - A category tag if the task has a category
3. Completed tasks will have:
   - Reduced opacity
   - Strikethrough on the title
   - Priority stripe remains fully visible
   - Badges/tags slightly faded

### Adding Tasks with Priority and Category
1. Click the "Add Task" button to open the task creation modal
2. Enter the task title and description
3. Select a priority level (High, Medium, Low) using the colored buttons
4. Optionally enter a category
5. Click "Save" to create the task

### Editing Tasks with Priority and Category
1. Click on an existing task to open the edit modal
2. The priority and category fields will be pre-filled with existing values
3. Modify the priority or category as needed
4. Click "Save" to update the task

## Available Components

The following components were updated or created:

- `TaskCard.tsx`: Enhanced with priority stripe, priority badge, and category tag
- `types/task.ts`: Updated Task interface with priority and category fields (if not already present)

## Example Usage

```
When viewing tasks:
- High priority tasks will have a red left stripe and HIGH badge
- Medium priority tasks will have a gold left stripe and MEDIUM badge
- Low priority tasks will have a gray left stripe and LOW badge
- Tasks with categories will display category tags
- Completed tasks will have reduced opacity with strikethrough titles
```

## Testing

To run the tests for the new functionality:

```bash
npm test
```

This will run both unit and integration tests for the updated components.