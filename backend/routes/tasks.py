from fastapi import APIRouter, Depends, HTTPException, Path, Query
from typing import List, Optional
from sqlmodel import Session, Field, select, SQLModel, case
from models import Task
from dependencies import get_current_user_id
from db import get_session
from datetime import datetime
from fastapi.responses import Response
from enum import Enum
from services.state_service import state_service
from constants import TASK_STATE_KEY_PATTERN

# Define the ReminderType enum to match the schema
class ReminderType(str, Enum):
    EMAIL = "email"
    PUSH = "push"
    SMS = "sms"
    BEFORE_DUE = "before_due"

# Define the TaskCreate model for new task requests
class TaskCreate(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    priority: Optional[str] = Field(default="medium", description="high | medium | low | urgent")
    category: Optional[str] = Field(default=None, max_length=50, description="e.g., work, personal, health, shopping")
    # New fields for Phase 5 - Advanced Features
    tags: Optional[List[str]] = Field(default=[], description="List of tags for the task")
    due_date: Optional[datetime] = Field(default=None, description="Due date for the task")
    is_recurring: Optional[bool] = Field(default=False, description="Whether the task repeats")
    recurrence_rule: Optional[str] = Field(default=None, max_length=200, description="RRULE format recurrence pattern")
    reminder_time: Optional[datetime] = Field(default=None, description="Time to send reminder")
    reminder_type: Optional[ReminderType] = Field(default=None, description="Type of reminder: email, push, sms, before_due")
    reminder_offset: Optional[int] = Field(default=None, description="Minutes before due date to send reminder")

# Define the TaskUpdate model for partial updates
class TaskUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    priority: Optional[str] = Field(default=None, description="high | medium | low | urgent")
    category: Optional[str] = Field(default=None, max_length=50, description="e.g., work, personal, health, shopping")
    completed: Optional[bool] = None
    # New fields for Phase 5 - Advanced Features
    tags: Optional[List[str]] = Field(default=None, description="List of tags for the task")
    due_date: Optional[datetime] = Field(default=None, description="Due date for the task")
    is_recurring: Optional[bool] = Field(default=None, description="Whether the task repeats")
    recurrence_rule: Optional[str] = Field(default=None, max_length=200, description="RRULE format recurrence pattern")
    next_occurrence: Optional[datetime] = Field(default=None, description="Next occurrence of recurring task")
    reminder_time: Optional[datetime] = Field(default=None, description="Time to send reminder")
    reminder_type: Optional[ReminderType] = Field(default=None, description="Type of reminder: email, push, sms, before_due")
    reminder_offset: Optional[int] = Field(default=None, description="Minutes before due date to send reminder")

router = APIRouter()

def get_task_or_404(task_id: int, user_id: str, session: Session) -> Task:
    """
    Helper function to fetch task with ownership verification
    """
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this task")
    return task

@router.get("/tasks", response_model=List[Task])
def list_tasks(
    user_id: str = Depends(get_current_user_id),
    status: Optional[str] = Query(None, description="Filter by status: all, pending, or completed"),
    priority: Optional[str] = Query(None, description="Filter by priority: all, high, medium, low, urgent"),
    category: Optional[str] = Query(None, description="Filter by category: all or specific category"),
    tags: Optional[str] = Query(None, description="Comma-separated list of tags to filter by"),
    q: Optional[str] = Query(None, description="Keyword to search in title and description"),
    sort: Optional[str] = Query("created", description="Sort by: created, title, priority, or category"),
    due_after: Optional[str] = Query(None, description="Filter tasks with due date after this date (YYYY-MM-DD)"),
    due_before: Optional[str] = Query(None, description="Filter tasks with due date before this date (YYYY-MM-DD)"),
    session: Session = Depends(get_session)
):
    # Base query filtered by authenticated user only
    statement = select(Task).where(Task.user_id == user_id)

    # Status filter
    if status == "pending":
        statement = statement.where(Task.completed == False)
    elif status == "completed":
        statement = statement.where(Task.completed == True)
    # "all" or None → no additional filter

    # Priority filter - can now accept multiple priorities
    if priority:
        priority_list = priority.split(',')
        statement = statement.where(Task.priority.in_(priority_list))

    # Category filter
    if category:
        statement = statement.where(Task.category == category)

    # Tags filter - can accept multiple tags
    if tags:
        tag_list = tags.split(',')
        for tag in tag_list:
            statement = statement.where(Task.tags.op('?')(tag.strip()))

    # Search in title and description
    if q:
        search_term = f"%{q}%"
        statement = statement.where((Task.title.ilike(search_term)) | (Task.description.ilike(search_term)))

    # Due date range filter
    if due_after:
        from datetime import datetime
        try:
            due_after_date = datetime.strptime(due_after, "%Y-%m-%d").date()
            statement = statement.where(Task.due_date >= due_after_date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid due_after date format. Use YYYY-MM-DD")

    if due_before:
        from datetime import datetime
        try:
            due_before_date = datetime.strptime(due_before, "%Y-%m-%d").date()
            statement = statement.where(Task.due_date <= due_before_date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid due_before date format. Use YYYY-MM-DD")

    # Sorting - can now accept multiple sort fields
    sort_fields = sort.split(',')
    order_clauses = []

    for sort_field in sort_fields:
        field_desc = sort_field.startswith('-')
        clean_field = sort_field.lstrip('-')

        if clean_field == "title":
            order_clause = Task.title.desc() if field_desc else Task.title.asc()
        elif clean_field == "priority":
            # Sort by priority: urgent, high, medium, low
            priority_order = case(
                [(Task.priority == "urgent", 1), (Task.priority == "high", 2),
                 (Task.priority == "medium", 3), (Task.priority == "low", 4)],
                else_=5
            )
            order_clause = priority_order.desc() if field_desc else priority_order.asc()
        elif clean_field == "due_date":
            order_clause = Task.due_date.desc() if field_desc else Task.due_date.asc()
        elif clean_field == "created_at":
            order_clause = Task.created_at.desc() if field_desc else Task.created_at.asc()
        else:  # default "created" → newest first
            order_clause = Task.created_at.desc() if field_desc else Task.created_at.asc()

        order_clauses.append(order_clause)

    statement = statement.order_by(*order_clauses)

    tasks = session.exec(statement).all()
    return tasks

@router.post("/tasks", response_model=Task)
def create_task(
    task_data: TaskCreate,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    new_task = Task(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority or "medium",
        category=task_data.category,
        completed=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        # New fields for Phase 5 - Advanced Features
        tags=task_data.tags or [],
        due_date=task_data.due_date,
        is_recurring=task_data.is_recurring or False,
        recurrence_rule=task_data.recurrence_rule,
        next_occurrence=None  # Will be calculated if it's a recurring task
    )

    # If it's a recurring task, calculate the next occurrence
    if new_task.is_recurring and new_task.recurrence_rule:
        from utils.recurrence_utils import calculate_next_occurrence
        if new_task.due_date:
            next_occurrence = calculate_next_occurrence(new_task.recurrence_rule, new_task.due_date)
            new_task.next_occurrence = next_occurrence

    session.add(new_task)
    session.commit()
    session.refresh(new_task)

    # Save task state to Dapr state store
    task_key = TASK_STATE_KEY_PATTERN.format(taskId=new_task.id)
    task_dict = new_task.dict()
    # Convert datetime objects to strings for JSON serialization
    for key, value in task_dict.items():
        if isinstance(value, datetime):
            task_dict[key] = value.isoformat()

    # Save to state store asynchronously
    import asyncio
    asyncio.create_task(state_service.save_state(task_key, task_dict))

    # Publish task created event
    from utils.event_publisher import EventPublisher
    from utils.notification_utils import send_task_notification
    publisher = EventPublisher()
    try:
        publisher.publish_task_event("created", new_task, user_id)

        # If the task has a due date, publish a reminder event
        if new_task.due_date:
            publisher.publish_reminder_event(new_task, user_id)

        # Send notification about the new task creation
        send_task_notification(
            session=session,
            user_id=user_id,
            task=new_task,
            event_type="task_created",
            custom_message=f"A new task '{new_task.title}' has been created!"
        )
    finally:
        publisher.close()

    return new_task

@router.get("/tasks/{task_id}", response_model=Task)
def get_task_by_id(
    task_id: int = Path(..., title="The ID of the task to retrieve"),
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    # First try to get from state store
    task_key = TASK_STATE_KEY_PATTERN.format(taskId=task_id)
    task_from_state = asyncio.run(state_service.get_state(task_key))

    if task_from_state:
        # If found in state store, return it
        # Convert datetime strings back to datetime objects if needed
        for key, value in task_from_state.items():
            if isinstance(value, str):
                try:
                    # Try to parse as ISO format datetime
                    from datetime import datetime
                    task_from_state[key] = datetime.fromisoformat(value.replace('Z', '+00:00'))
                except ValueError:
                    # If not a datetime string, keep as is
                    pass
        return Task(**task_from_state)
    else:
        # If not in state store, get from database
        task = get_task_or_404(task_id, user_id, session)
        return task

@router.put("/tasks/{task_id}", response_model=Task)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    task = get_task_or_404(task_id, user_id, session)

    # Update task fields only if they're provided in the request
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.priority is not None:
        task.priority = task_data.priority
    if task_data.category is not None:
        task.category = task_data.category
    if task_data.completed is not None:
        task.completed = task_data.completed
    # New fields for Phase 5 - Advanced Features
    if task_data.tags is not None:
        task.tags = task_data.tags
    if task_data.due_date is not None:
        task.due_date = task_data.due_date
    if task_data.is_recurring is not None:
        task.is_recurring = task_data.is_recurring
    if task_data.recurrence_rule is not None:
        task.recurrence_rule = task_data.recurrence_rule
    if task_data.next_occurrence is not None:
        task.next_occurrence = task_data.next_occurrence
    if task_data.reminder_time is not None:
        task.reminder_time = task_data.reminder_time
    if task_data.reminder_type is not None:
        task.reminder_type = task_data.reminder_type
    if task_data.reminder_offset is not None:
        task.reminder_offset = task_data.reminder_offset

    # If it's a recurring task, calculate the next occurrence
    if task.is_recurring and task.recurrence_rule:
        from utils.recurrence_utils import calculate_next_occurrence

        if task.due_date:
            next_occurrence = calculate_next_occurrence(task.recurrence_rule, task.due_date)
            task.next_occurrence = next_occurrence

    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    # Update task state in Dapr state store
    task_key = TASK_STATE_KEY_PATTERN.format(taskId=task.id)
    task_dict = task.dict()
    # Convert datetime objects to strings for JSON serialization
    for key, value in task_dict.items():
        if isinstance(value, datetime):
            task_dict[key] = value.isoformat()

    # Update state store asynchronously
    import asyncio
    asyncio.create_task(state_service.save_state(task_key, task_dict))

    # Publish task updated event
    from utils.event_publisher import EventPublisher
    from utils.notification_utils import send_task_notification

    publisher = EventPublisher()
    try:
        publisher.publish_task_event("updated", task, user_id)

        # If the task has a due date, publish a reminder event
        if task.due_date:
            publisher.publish_reminder_event(task, user_id)

        # Send notification about the task update
        send_task_notification(
            session=session,
            user_id=user_id,
            task=task,
            event_type="task_updated",
            custom_message=f"The task '{task.title}' has been updated."
        )
    finally:
        publisher.close()

    return task

@router.delete("/tasks/{task_id}", status_code=204)
def delete_task(
    task_id: int,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    task = get_task_or_404(task_id, user_id, session)

    # Delete task state from Dapr state store
    task_key = TASK_STATE_KEY_PATTERN.format(taskId=task_id)
    import asyncio
    asyncio.create_task(state_service.delete_state(task_key))

    session.delete(task)
    session.commit()
    return Response(status_code=204)

@router.patch("/tasks/{task_id}/complete", response_model=Task)
def toggle_complete(
    task_id: int,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    task = get_task_or_404(task_id, user_id, session)

    # Toggle completion status
    task.completed = not task.completed
    task.updated_at = datetime.utcnow()

    # If this is a recurring task and we're marking it as complete,
    # we need to create the next instance
    if task.completed and task.is_recurring and task.recurrence_rule:
        from utils.recurrence_utils import calculate_next_occurrence

        # Calculate the next occurrence based on the recurrence rule
        if task.next_occurrence:
            next_date = task.next_occurrence
        elif task.due_date:
            next_date = calculate_next_occurrence(task.recurrence_rule, task.due_date)
        else:
            next_date = calculate_next_occurrence(task.recurrence_rule, datetime.utcnow())

        if next_date:
            # Create the next instance of the recurring task
            next_task = Task(
                user_id=task.user_id,
                title=task.title,
                description=task.description,
                priority=task.priority,
                category=task.category,
                tags=task.tags,
                due_date=next_date,
                is_recurring=task.is_recurring,
                recurrence_rule=task.recurrence_rule,
                completed=False,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

            # Calculate the next occurrence for the new task
            if task.recurrence_rule:
                next_occurrence = calculate_next_occurrence(task.recurrence_rule, next_date)
                next_task.next_occurrence = next_occurrence

            session.add(next_task)
            session.commit()

            # Save new task to state store
            task_key = TASK_STATE_KEY_PATTERN.format(taskId=next_task.id)
            task_dict = next_task.dict()
            # Convert datetime objects to strings for JSON serialization
            for key, value in task_dict.items():
                if isinstance(value, datetime):
                    task_dict[key] = value.isoformat()

            # Save to state store asynchronously
            import asyncio
            asyncio.create_task(state_service.save_state(task_key, task_dict))

            # Publish task created event for the new recurring instance
            from utils.event_publisher import EventPublisher

            publisher = EventPublisher()
            try:
                publisher.publish_task_event("created", next_task, user_id)

                # If the next task has a due date, publish a reminder event
                if next_task.due_date:
                    publisher.publish_reminder_event(next_task, user_id)
            finally:
                publisher.close()

    session.add(task)
    session.commit()
    session.refresh(task)

    # Update task state in Dapr state store
    task_key = TASK_STATE_KEY_PATTERN.format(taskId=task.id)
    task_dict = task.dict()
    # Convert datetime objects to strings for JSON serialization
    for key, value in task_dict.items():
        if isinstance(value, datetime):
            task_dict[key] = value.isoformat()

    # Update state store asynchronously
    import asyncio
    asyncio.create_task(state_service.save_state(task_key, task_dict))

    # Publish task completed event
    from utils.event_publisher import EventPublisher
    from utils.notification_utils import send_task_notification

    publisher = EventPublisher()
    try:
        publisher.publish_task_event("completed", task, user_id)

        # Send notification about the task completion
        send_task_notification(
            session=session,
            user_id=user_id,
            task=task,
            event_type="task_completed",
            custom_message=f"The task '{task.title}' has been marked as completed!"
        )
    finally:
        publisher.close()

    return task