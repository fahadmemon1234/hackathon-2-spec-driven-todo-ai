# CLI Command Contracts: Todo CLI App

**Feature**: Todo CLI App
**Date**: 2025-12-27
**Branch**: 1-todo-cli-app

## Command Interface Specification

This document specifies the contract for the CLI commands of the Todo application.

### Add Command
**Command**: `add <title> <description>`
**Input**: 
- title: string (1-100 characters)
- description: string (0-500 characters)
**Output**: 
- Success: "Task added with ID: {id}"
- Error: Appropriate error message
**Behavior**: Creates a new task with the provided title and description, assigns a unique ID, and sets completion status to false.

### List Command
**Command**: `list`
**Input**: None
**Output**: 
- Success: List of all tasks with ID, title, description, and completion status
- Error: Appropriate error message
**Behavior**: Displays all tasks in the system with their details.

### Update Command
**Command**: `update <id> <title> <description>`
**Input**: 
- id: integer (positive)
- title: string (1-100 characters)
- description: string (0-500 characters)
**Output**: 
- Success: "Task {id} updated successfully"
- Error: Appropriate error message
**Behavior**: Updates the title and description of the task with the specified ID.

### Delete Command
**Command**: `delete <id>`
**Input**: 
- id: integer (positive)
**Output**: 
- Success: "Task {id} deleted successfully"
- Error: Appropriate error message
**Behavior**: Removes the task with the specified ID from the system.

### Complete Command
**Command**: `complete <id>`
**Input**: 
- id: integer (positive)
**Output**: 
- Success: "Task {id} marked as complete"
- Error: Appropriate error message
**Behavior**: Changes the completion status of the task with the specified ID to true.

### Incomplete Command
**Command**: `incomplete <id>`
**Input**: 
- id: integer (positive)
**Output**: 
- Success: "Task {id} marked as incomplete"
- Error: Appropriate error message
**Behavior**: Changes the completion status of the task with the specified ID to false.

### Help Command
**Command**: `help`
**Input**: None
**Output**: List of available commands with brief descriptions
**Behavior**: Displays help information about available commands.

### Quit/Exit Commands
**Command**: `quit` or `exit`
**Input**: None
**Output**: "Goodbye!"
**Behavior**: Terminates the application.

## Error Handling Contracts

### Invalid Command
**Condition**: User enters an unrecognized command
**Response**: Display "Unknown command: {command}. Type 'help' for available commands."

### Invalid Task ID
**Condition**: User provides a non-existent task ID
**Response**: Display "Task with ID {id} does not exist."

### Invalid Parameters
**Condition**: User provides incorrect number or type of parameters
**Response**: Display appropriate error message with usage instructions.

### Input Validation Errors
**Condition**: User provides input that violates validation rules (e.g., title too long)
**Response**: Display specific validation error message.