"""
Recurring Task Service

This service consumes task-events and handles recurring task logic.
When a recurring task is marked as completed, it creates the next instance
according to the recurrence rule.
"""

import asyncio
import json
import os
from datetime import datetime
from typing import Dict, Any

import sys
import os
# Add the backend directory to the path so we can import from utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dateutil.rrule import rrulestr
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select

from backend.database import engine
from backend.models.task import Task

load_dotenv()

app = FastAPI(title="Recurring Task Service")

@app.post("/process_completed_task")
async def process_completed_task(event_data: Dict[Any, Any]):
    """
    Process a completed task event and create the next instance if it's recurring
    """
    task_id = event_data.get("task_id")
    task_data = event_data.get("task_data")
    
    if not task_data or not task_data.get("is_recurring"):
        # Not a recurring task, nothing to do
        return {"message": "Task is not recurring, skipping"}
    
    # Extract recurrence information
    recurrence_rule = task_data.get("recurrence_rule")
    if not recurrence_rule:
        raise HTTPException(status_code=400, detail="Recurring task missing recurrence rule")
    
    # Calculate next occurrence based on recurrence rule
    completed_at = datetime.fromisoformat(task_data["updated_at"].replace('Z', '+00:00'))
    next_occurrence = calculate_next_occurrence(recurrence_rule, completed_at)
    
    # Create the next instance of the recurring task
    next_task = Task(
        user_id=task_data["user_id"],
        title=task_data["title"],
        description=task_data["description"],
        priority=task_data["priority"],
        tags=task_data["tags"],
        due_date=next_occurrence,  # Set due date to next occurrence
        is_recurring=task_data["is_recurring"],
        recurrence_rule=task_data["recurrence_rule"],
        next_occurrence=calculate_next_occurrence(recurrence_rule, next_occurrence)
    )
    
    # Save the next task instance to the database
    with Session(engine) as session:
        session.add(next_task)
        session.commit()
        session.refresh(next_task)
    
    return {
        "message": f"Created next instance of recurring task {task_id}",
        "next_task_id": next_task.id,
        "next_occurrence": next_occurrence.isoformat()
    }


def calculate_next_occurrence(recurrence_rule: str, start_date: datetime) -> datetime:
    """
    Calculate the next occurrence based on the recurrence rule.
    recurrence_rule format: "FREQ=DAILY", "FREQ=WEEKLY;BYDAY=MO,WE", etc.
    """
    try:
        rule = rrulestr(recurrence_rule, dtstart=start_date)
        next_occurrence = next(rule.after(start_date))
        return next_occurrence
    except Exception as e:
        raise ValueError(f"Invalid recurrence rule: {e}")


@app.get("/")
def read_root():
    return {"service": "Recurring Task Service", "status": "running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)