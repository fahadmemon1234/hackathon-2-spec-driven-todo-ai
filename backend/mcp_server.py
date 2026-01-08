from mcp.server.fastmcp import FastMCP
from mcp.server import NotificationOptions
from models import Task, Conversation, Message
from db import get_session
from sqlmodel import select
import datetime
from contextlib import contextmanager

# Create the MCP server instance
mcp = FastMCP("Todo Task Manager")

@contextmanager
def get_db_session():
    """Context manager to get database session"""
    try:
        session_gen = get_session()
        session = next(session_gen)
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

@mcp.tool()
def add_task(
    user_id: str,
    title: str,
    description: str | None = None
) -> dict:
    """
    Create a new task for the authenticated user.
    """
    with get_db_session() as session:
        # Create new task
        task = Task(
            user_id=user_id,
            title=title,
            description=description,
            completed=False
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        
        return {
            "task_id": task.id,
            "status": "created",
            "title": task.title,
            "description": task.description
        }


@mcp.tool()
def list_tasks(
    user_id: str,
    status: str = "all"
) -> list:
    """
    List tasks for the authenticated user with optional filtering.
    """
    with get_db_session() as session:
        # Build query based on status filter
        query = select(Task).where(Task.user_id == user_id)
        
        if status == "pending":
            query = query.where(Task.completed == False)
        elif status == "completed":
            query = query.where(Task.completed == True)
        
        tasks = session.exec(query).all()
        
        # Convert tasks to the required format
        result = []
        for task in tasks:
            result.append({
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat() if task.created_at else None
            })
        
        return result


@mcp.tool()
def update_task(
    user_id: str,
    task_id: int,
    title: str | None = None,
    description: str | None = None
) -> dict:
    """
    Update task title/description for the authenticated user.
    """
    with get_db_session() as session:
        # Get the task
        task = session.exec(select(Task).where(Task.id == task_id).where(Task.user_id == user_id)).first()
        
        if not task:
            raise ValueError(f"Task with ID {task_id} not found or does not belong to user")
        
        # Update fields if provided
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
            
        session.add(task)
        session.commit()
        session.refresh(task)
        
        return {
            "task_id": task.id,
            "status": "updated",
            "title": task.title
        }


@mcp.tool()
def complete_task(
    user_id: str,
    task_id: int
) -> dict:
    """
    Mark a task as completed for the authenticated user.
    """
    with get_db_session() as session:
        # Get the task
        task = session.exec(select(Task).where(Task.id == task_id).where(Task.user_id == user_id)).first()
        
        if not task:
            raise ValueError(f"Task with ID {task_id} not found or does not belong to user")
        
        # Mark as completed
        task.completed = True
        session.add(task)
        session.commit()
        session.refresh(task)
        
        return {
            "task_id": task.id,
            "status": "completed",
            "title": task.title
        }


@mcp.tool()
def delete_task(
    user_id: str,
    task_id: int
) -> dict:
    """
    Delete a task for the authenticated user.
    """
    with get_db_session() as session:
        # Get the task
        task = session.exec(select(Task).where(Task.id == task_id).where(Task.user_id == user_id)).first()
        
        if not task:
            raise ValueError(f"Task with ID {task_id} not found or does not belong to user")
        
        # Delete the task
        session.delete(task)
        session.commit()
        
        return {
            "task_id": task.id,
            "status": "deleted",
            "title": task.title
        }