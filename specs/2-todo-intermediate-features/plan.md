# Implementation Plan: Todo App Intermediate Features

## Technical Context

**Feature**: Intermediate Level Features for Todo In-Memory Python Console App (Phase I Extension)
**Branch**: 2-todo-intermediate-features
**Spec**: specs/2-todo-intermediate-features/spec.md

### Current Architecture
- Existing foundation: Basic todo app with Add, Delete, Update, View, Mark Complete
- Storage: In-memory only using Python objects
- CLI interface: Console-based interactive application
- Code location: /src directory
- Technology: Python 3.13+, standard library only

### New Features to Implement
1. Priorities – Assign priority levels (High, Medium, Low) to tasks during creation or update
2. Tags/Categories – Allow multiple tags per task (e.g., "work", "personal", "shopping")
3. Search & Filter – Search by keyword (title/description/tags) and filter by status, priority, or tag
4. Sort Tasks – Support sorting when listing (by priority, completion status, or title alphabetically)

### Dependencies
- Python 3.13+
- Standard library only (no external dependencies)
- UV for package management

### Integration Points
- Extend existing Task model in /src
- Update TodoManager functionality
- Enhance CLI interface
- Maintain backward compatibility with existing features

## Constitution Check

### Project Constitution Adherence
- [x] AI-only coding (Claude Code primary, Qwen for planning/validation)
- [x] Clean architecture principles
- [x] Modularity for future phases
- [x] Type hints and docstrings
- [x] Proper error handling
- [x] Standard library only (no external dependencies)
- [x] In-memory storage only (no persistence)
- [x] CLI interface only (no GUI/network features)

### Gates
- [x] Technology stack compliance (Python 3.13+, standard library)
- [x] Storage compliance (in-memory only)
- [x] Interface compliance (command-line only)
- [x] Project structure compliance (add/modify files only within /src)

## Phase 0: Outline & Research

### Research Tasks

#### 1. Task Model Extension Research
**Decision**: How to extend the existing Task model to include priority and tags
**Rationale**: Need to determine the best approach to add priority and tags fields to the existing Task model
**Alternatives considered**: 
- Adding fields directly to the existing model
- Creating a new Task model that extends the existing one
- Using composition to add priority and tags

#### 2. Priority Implementation Research
**Decision**: How to implement priority levels (High, Medium, Low)
**Rationale**: Need to determine the best way to represent priority levels in code
**Alternatives considered**:
- Using string constants
- Using an Enum class
- Using integer values

#### 3. Tags Implementation Research
**Decision**: How to implement multiple tags per task
**Rationale**: Need to determine the best data structure to store multiple tags
**Alternatives considered**:
- Using a list of strings
- Using a set of strings
- Using a custom Tag class

#### 4. CLI Interface Enhancement Research
**Decision**: How to enhance the CLI interface to support new features
**Rationale**: Need to determine the best way to expose new functionality to users
**Alternatives considered**:
- Adding flags to existing commands (e.g., `list --sort priority`)
- Adding new dedicated commands (e.g., `search`, `filter`)
- Modifying existing command prompts

## Phase 1: Design & Contracts

### Data Model: data-model.md

#### Updated Task Entity
```
Entity: Task
- id: int (unique identifier)
- title: str (task title)
- description: str (optional task description)
- completed: bool (completion status)
- priority: str (priority level: "High", "Medium", "Low")
- tags: set[str] (collection of tags)
```

#### Priority Enum
```
Enum: Priority
- HIGH = "High"
- MEDIUM = "Medium" 
- LOW = "Low"
```

### API Contracts

#### CLI Commands
1. `add <title> --priority <level> --tags <tag1,tag2,...>`
   - Adds a new task with specified priority and tags
   - Example: `add "Buy groceries" --priority High --tags shopping,urgent`

2. `list [--sort <field>] [--filter <type:value>] [--search <keyword>]`
   - Lists tasks with optional sorting, filtering, and searching
   - Examples: 
     - `list --sort priority` (sort by priority)
     - `list --filter status:completed` (show only completed tasks)
     - `list --filter priority:High` (show only high priority tasks)
     - `list --search "grocery"` (search for keyword in title/description/tags)

3. `update <id> --priority <level> --tags <tag1,tag2,...>`
   - Updates an existing task with new priority and tags
   - Example: `update 1 --priority Medium --tags work,important`

4. `search <keyword>`
   - Searches for tasks containing the keyword
   - Example: `search "project"`

### Quickstart Guide: quickstart.md

#### Setting up the enhanced todo app
1. Clone the repository
2. Install dependencies with UV: `uv sync`
3. Run the application: `python -m src.main`

#### Using new features
1. Add a task with priority and tags:
   ```
   add "Complete project proposal" --priority High --tags work,important
   ```

2. List tasks sorted by priority:
   ```
   list --sort priority
   ```

3. Filter tasks by tag:
   ```
   list --filter tag:work
   ```

4. Search for tasks:
   ```
   search "project"
   ```

## Phase 2: Implementation Plan

### Task Breakdown

#### Task 1: Extend Task Model with Priority and Tags
- **File**: src/models.py (or update existing task model file)
- **Description**: Add priority and tags fields to the existing Task model
- **Expected outcome**: Task objects can store priority level and multiple tags

#### Task 2: Update TodoManager with New Operations
- **File**: src/todo_manager.py (or existing manager file)
- **Description**: Add methods for searching, filtering, and sorting tasks
- **Expected outcome**: TodoManager can perform all new operations on tasks

#### Task 3: Enhance CLI Interface for New Features
- **File**: src/cli.py (or main application file)
- **Description**: Update command parsing to handle new flags and commands
- **Expected outcome**: Users can use new features via CLI commands

#### Task 4: Update Task Creation to Accept Priority and Tags
- **File**: src/cli.py and src/todo_manager.py
- **Description**: Modify add_task functionality to accept priority and tags
- **Expected outcome**: New tasks can be created with priority and tags

#### Task 5: Update Task Update to Modify Priority and Tags
- **File**: src/cli.py and src/todo_manager.py
- **Description**: Modify update_task functionality to change priority and tags
- **Expected outcome**: Existing tasks can have their priority and tags updated

#### Task 6: Implement Search Functionality
- **File**: src/todo_manager.py and src/cli.py
- **Description**: Add search method that looks for keywords in title, description, and tags
- **Expected outcome**: Users can search for tasks by keyword

#### Task 7: Implement Filter Functionality
- **File**: src/todo_manager.py and src/cli.py
- **Description**: Add filter method that filters tasks by status, priority, or tag
- **Expected outcome**: Users can filter tasks by various criteria

#### Task 8: Implement Sort Functionality
- **File**: src/todo_manager.py and src/cli.py
- **Description**: Add sort method that sorts tasks by priority, status, or title
- **Expected outcome**: Users can sort task lists by various criteria

#### Task 9: Enhance Task Display to Show New Information
- **File**: src/cli.py
- **Description**: Update list display to show priority, tags, and status indicators
- **Expected outcome**: Task list shows all relevant information clearly

#### Task 10: Add Comprehensive Error Handling
- **File**: All relevant files
- **Description**: Add validation and error handling for new features
- **Expected outcome**: Appropriate error messages for invalid inputs

#### Task 11: Update Documentation and Help Text
- **File**: src/cli.py and README.md
- **Description**: Update help text and documentation to reflect new features
- **Expected outcome**: Users can understand how to use new features

#### Task 12: Testing and Integration
- **File**: All files
- **Description**: Test all new functionality and ensure backward compatibility
- **Expected outcome**: All features work correctly and existing functionality is preserved

## Implementation Order

1. **Task 1**: Extend Task Model with Priority and Tags
2. **Task 2**: Update TodoManager with New Operations
3. **Task 4**: Update Task Creation to Accept Priority and Tags
4. **Task 5**: Update Task Update to Modify Priority and Tags
5. **Task 9**: Enhance Task Display to Show New Information
6. **Task 6**: Implement Search Functionality
7. **Task 7**: Implement Filter Functionality
8. **Task 8**: Implement Sort Functionality
9. **Task 3**: Enhance CLI Interface for New Features
10. **Task 10**: Add Comprehensive Error Handling
11. **Task 11**: Update Documentation and Help Text
12. **Task 12**: Testing and Integration

## Milestones

### Milestone 1: Basic Enhancement
- Tasks 1-5 completed
- Can create and update tasks with priority and tags
- Can view tasks with enhanced display

### Milestone 2: Advanced Features
- Tasks 6-8 completed
- Can search, filter, and sort tasks
- All core functionality implemented

### Milestone 3: Complete Implementation
- All tasks completed
- Full feature set working
- Backward compatibility maintained
- Error handling in place

## Re-evaluation of Constitution Check

### Post-Implementation Compliance
- [x] All new code follows clean architecture principles
- [x] Type hints and docstrings added to all new functions
- [x] Error handling implemented properly
- [x] Standard library only used (no external dependencies)
- [x] In-memory storage maintained (no persistence added)
- [x] CLI interface only (no GUI/network features added)
- [x] Backward compatibility with existing features maintained