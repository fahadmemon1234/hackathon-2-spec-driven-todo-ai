# API Contracts: TaskCard Priority & Category Visual Display

**Feature**: TaskCard Priority & Category Visual Display
**Date**: 2026-01-02
**Branch**: 13-taskcard-priority-category

## Task API Contract

This document specifies the contract for the Task API endpoints that support priority and category fields for display in the TaskCard component.

### Get Task Endpoint
**Endpoint**: `GET /api/tasks/{id}`
**Input**: None
**Output**:
```json
{
  "id": "string",
  "title": "string",
  "description": "string",
  "completed": "boolean",
  "created_at": "string (ISO date)",
  "updated_at": "string (ISO date)",
  "priority": "string",
  "category": "string (optional)"
}
```
**Success Response**: 200 OK
**Error Response**: 404 Not Found (task doesn't exist)

### Get All Tasks Endpoint
**Endpoint**: `GET /api/tasks`
**Input**: None
**Output**:
```json
[
  {
    "id": "string",
    "title": "string",
    "description": "string",
    "completed": "boolean",
    "created_at": "string (ISO date)",
    "updated_at": "string (ISO date)",
    "priority": "string",
    "category": "string (optional)"
  }
]
```
**Success Response**: 200 OK

### Update Task Endpoint
**Endpoint**: `PUT /api/tasks/{id}`
**Input**:
```json
{
  "title": "string (required, 1-100 chars)",
  "description": "string (optional, 0-500 chars)",
  "priority": "string (required, one of: 'high', 'medium', 'low')",
  "category": "string (optional, 0-50 chars)",
  "completed": "boolean"
}
```
**Output**:
```json
{
  "id": "string",
  "title": "string",
  "description": "string",
  "completed": "boolean",
  "created_at": "string (ISO date)",
  "updated_at": "string (ISO date)",
  "priority": "string",
  "category": "string (optional)"
}
```
**Success Response**: 200 OK
**Error Response**: 400 Bad Request (validation errors), 404 Not Found (task doesn't exist)

## Validation Contracts

### Priority Validation
**Condition**: Priority value must be one of "high", "medium", or "low"
**Response**: 400 Bad Request with error message "Priority must be one of: high, medium, low"

### Category Validation
**Condition**: Category, if provided, must be between 1 and 50 characters
**Response**: 400 Bad Request with error message "Category must be between 1 and 50 characters"

### Default Values
**Condition**: When retrieving a task without priority specified
**Behavior**: System returns default priority value "medium"