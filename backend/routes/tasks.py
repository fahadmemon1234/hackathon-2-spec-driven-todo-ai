from fastapi import APIRouter, Depends, HTTPException, Path, Query
from typing import List, Optional
from sqlmodel import Session, Field, select, SQLModel, case
from models import Task
from dependencies import get_current_user_id
from db import get_session
from datetime import datetime
from fastapi.responses import Response

# Define the TaskCreate model for new task requests
class TaskCreate(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    priority: Optional[str] = Field(default="medium", description="high | medium | low")
    category: Optional[str] = Field(default=None, max_length=50, description="e.g., work, personal, health, shopping")

# Define the TaskUpdate model for partial updates
class TaskUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    priority: Optional[str] = Field(default=None, description="high | medium | low")
    category: Optional[str] = Field(default=None, max_length=50, description="e.g., work, personal, health, shopping")
    completed: Optional[bool] = None

router = APIRouter(prefix="/api")

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
    priority: Optional[str] = Query(None, description="Filter by priority: all, high, medium, low"),
    category: Optional[str] = Query(None, description="Filter by category: all or specific category"),
    sort: Optional[str] = Query("created", description="Sort by: created, title, priority, or category"),
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

    # Priority filter
    if priority:
        statement = statement.where(Task.priority == priority)

    # Category filter
    if category:
        statement = statement.where(Task.category == category)

    # Sorting
    if sort == "title":
        statement = statement.order_by(Task.title)
    elif sort == "priority":
        # Sort by priority: high, medium, low
        statement = statement.order_by(
            case(
                [(Task.priority == "high", 1), (Task.priority == "medium", 2)],
                else_=3
            ),
            Task.created_at.desc()
        )
    elif sort == "category":
        statement = statement.order_by(Task.category, Task.created_at.desc())
    else:  # default "created" → newest first
        statement = statement.order_by(Task.created_at.desc())

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
        updated_at=datetime.utcnow()
    )
    session.add(new_task)
    session.commit()
    session.refresh(new_task)
    return new_task

@router.get("/tasks/{task_id}", response_model=Task)
def get_task_by_id(
    task_id: int = Path(..., title="The ID of the task to retrieve"),
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
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
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.delete("/tasks/{task_id}", status_code=204)
def delete_task(
    task_id: int,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    task = get_task_or_404(task_id, user_id, session)
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

    session.add(task)
    session.commit()
    session.refresh(task)
    return task