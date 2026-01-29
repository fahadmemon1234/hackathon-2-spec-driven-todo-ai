from datetime import datetime, timedelta
from typing import Optional
from sqlmodel import Session, select
from backend.models import Task
from schemas.task_update import UpdateTaskRequest


def calculate_next_occurrence(recurrence_rule: str, current_date: datetime) -> Optional[datetime]:
    """
    Calculate the next occurrence based on the recurrence rule.
    Supports daily, weekly, monthly, yearly patterns.
    """
    if not recurrence_rule:
        return None
    
    # Parse recurrence rule (simple format: DAILY, WEEKLY, MONTHLY, YEARLY)
    rule = recurrence_rule.upper()
    
    if rule == "DAILY":
        return current_date + timedelta(days=1)
    elif rule == "WEEKLY":
        return current_date + timedelta(weeks=1)
    elif rule == "MONTHLY":
        # Simple monthly calculation (adding ~30 days)
        return current_date + timedelta(days=30)
    elif rule == "YEARLY":
        return current_date + timedelta(days=365)
    else:
        # For more complex rules, you might want to use a library like dateutil
        # For now, return None for unsupported rules
        return None


def update_task(session: Session, task_id: str, user_id: str, task_update: UpdateTaskRequest) -> Optional[Task]:
    """
    Update a task with the provided fields.
    Only the task owner can update the task.
    """
    # Retrieve the existing task
    existing_task = session.get(Task, task_id)
    
    if not existing_task:
        return None
    
    # Check if the user owns the task
    if existing_task.user_id != user_id:
        return None
    
    # Update fields that are provided in the request
    update_data = task_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        if hasattr(existing_task, field):
            setattr(existing_task, field, value)
    
    # Update the updated_at timestamp
    existing_task.updated_at = datetime.now()
    
    # If the task is recurring, calculate the next occurrence
    if existing_task.is_recurring and existing_task.recurrence_rule:
        existing_task.next_occurrence = calculate_next_occurrence(
            existing_task.recurrence_rule, 
            existing_task.updated_at
        )
    
    # Commit the changes to the database
    session.add(existing_task)
    session.commit()
    session.refresh(existing_task)
    
    return existing_task