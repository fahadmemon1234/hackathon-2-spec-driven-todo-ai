from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from typing import Optional
from db import get_session
from dependencies import get_current_user_id
from schemas.task_update import UpdateTaskRequest, TaskResponse
from crud.task_update import update_task
from backend.models import Task

router = APIRouter()


@router.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task_endpoint(
    task_id: str,
    task_update: UpdateTaskRequest,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Update a task with the provided fields.
    Only the task owner can update the task.
    """
    try:
        # Attempt to update the task
        updated_task = update_task(
            session=session,
            task_id=task_id,
            user_id=user_id,
            task_update=task_update
        )
        
        if not updated_task:
            raise HTTPException(
                status_code=404,
                detail="Task not found or you don't have permission to update this task"
            )
        
        return updated_task
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while updating the task: {str(e)}"
        )


# Include additional helper endpoints if needed
@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: str,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Get a specific task by ID.
    Only the task owner can retrieve the task.
    """
    task = session.get(Task, task_id)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to access this task"
        )
    
    return task