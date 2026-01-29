from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from typing import Optional
import logging
import json
from datetime import datetime, timedelta
from sqlmodel import SQLModel, Field, create_engine, Session, select
import sys
import os
# Add the backend directory to the path so we can import from models
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))
from backend.models import Task
from dateutil.rrule import rrulestr
# Import recurrence utils from backend
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend', 'utils'))
from recurrence_utils import calculate_next_occurrence

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database setup - in a real implementation, this would come from environment
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
engine = create_engine(DATABASE_URL)

app = FastAPI(title="Recurring Task Service")

class TaskEvent(BaseModel):
    event_type: str
    task_id: int
    user_id: str
    task_data: dict
    timestamp: Optional[str] = None

@app.post("/dapr/subscribe/task-events")
async def handle_task_event_subscription(task_event: TaskEvent, background_tasks: BackgroundTasks):
    """
    Dapr subscription endpoint for task events.
    This endpoint receives task events from the 'task-events' topic.
    """
    logger.info(f"Received task event: {task_event.event_type} for task {task_event.task_id}")
    
    if task_event.event_type == "completed" and task_event.task_data.get('is_recurring'):
        # Schedule recurring task creation in background to avoid blocking Dapr
        background_tasks.add_task(create_next_recurring_instance, task_event)
        logger.info(f"Scheduled next recurring instance creation for task {task_event.task_id}")
        return {"status": "scheduled"}
    else:
        logger.info(f"Event {task_event.event_type} for task {task_event.task_id} does not require action")
        return {"status": "processed"}

def create_next_recurring_instance(task_event: TaskEvent):
    """
    Create the next instance of a recurring task
    """
    try:
        logger.info(f"Creating next recurring instance for task {task_event.task_id}")
        
        # Extract task data from the event
        task_data = task_event.task_data
        user_id = task_event.user_id
        
        # Calculate next occurrence based on recurrence rule
        if task_data.get('recurrence_rule'):
            next_date = calculate_next_occurrence(
                task_data['recurrence_rule'], 
                datetime.fromisoformat(task_data['due_date'].replace('Z', '+00:00')) if task_data.get('due_date') else datetime.utcnow()
            )
        else:
            # Fallback: add 1 day if no recurrence rule
            next_date = datetime.utcnow() + timedelta(days=1)
        
        if next_date:
            # Create new task instance in the database
            with Session(engine) as session:
                new_task = Task(
                    user_id=user_id,
                    title=task_data['title'],
                    description=task_data.get('description'),
                    priority=task_data.get('priority', 'medium'),
                    category=task_data.get('category'),
                    tags=task_data.get('tags', []),
                    due_date=next_date,
                    is_recurring=task_data.get('is_recurring', False),
                    recurrence_rule=task_data.get('recurrence_rule'),
                    completed=False,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                
                # Calculate the next occurrence for the new task
                if task_data.get('recurrence_rule'):
                    next_occurrence = calculate_next_occurrence(task_data['recurrence_rule'], next_date)
                    new_task.next_occurrence = next_occurrence
                
                session.add(new_task)
                session.commit()
                session.refresh(new_task)
                
                logger.info(f"Created next recurring instance for task {task_event.task_id} due {next_date}")
                
                # Publish event for the newly created task
                sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend', 'utils'))
                from event_publisher import EventPublisher
                publisher = EventPublisher()
                try:
                    publisher.publish_task_event("created", new_task, user_id)
                finally:
                    publisher.close()
        else:
            logger.warning(f"Could not calculate next occurrence for task {task_event.task_id}")
    
    except Exception as e:
        logger.error(f"Error creating next recurring instance for task {task_event.task_id}: {e}")

@app.get("/")
def read_root():
    return {"message": "Recurring Task Service Running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)