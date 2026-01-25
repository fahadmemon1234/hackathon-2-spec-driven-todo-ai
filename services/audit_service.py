from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List
import logging
from datetime import datetime
from sqlmodel import SQLModel, Field, create_engine, Session, select
from sqlalchemy import create_engine as create_sql_engine
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database setup - in a real implementation, this would come from environment
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./audit.db")
engine = create_sql_engine(DATABASE_URL)

app = FastAPI(title="Audit Service")

class AuditLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    event_type: str = Field(max_length=50)  # created, updated, completed, deleted
    task_id: int
    user_id: str
    task_data: str  # JSON string representation of task data
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class TaskEvent(BaseModel):
    event_type: str
    task_id: int
    user_id: str
    task_data: dict
    timestamp: Optional[str] = None

@app.post("/dapr/subscribe/task-events")
async def handle_task_event_subscription(task_event: TaskEvent):
    """
    Dapr subscription endpoint for task events.
    This endpoint receives task events from the 'task-events' topic and stores them in audit log.
    """
    logger.info(f"Received task event for audit: {task_event.event_type} for task {task_event.task_id}")
    
    # Create audit log entry
    audit_log = AuditLog(
        event_type=task_event.event_type,
        task_id=task_event.task_id,
        user_id=task_event.user_id,
        task_data=str(task_event.task_data),  # Convert to string for storage
        timestamp=datetime.utcnow()
    )
    
    # Save to database
    with Session(engine) as session:
        session.add(audit_log)
        session.commit()
        session.refresh(audit_log)
    
    logger.info(f"Audit log created for task {task_event.task_id}, event: {task_event.event_type}")
    return {"status": "logged", "audit_id": audit_log.id}

@app.get("/audit")
async def get_audit_logs(user_id: str = None, event_type: str = None, limit: int = 100):
    """
    Get audit logs with optional filters
    """
    logger.info(f"Fetching audit logs - user_id: {user_id}, event_type: {event_type}, limit: {limit}")
    
    with Session(engine) as session:
        query = select(AuditLog).order_by(AuditLog.timestamp.desc()).limit(limit)
        
        if user_id:
            query = query.where(AuditLog.user_id == user_id)
        if event_type:
            query = query.where(AuditLog.event_type == event_type)
        
        audit_logs = session.exec(query).all()
        
        return [
            {
                "id": log.id,
                "event_type": log.event_type,
                "task_id": log.task_id,
                "user_id": log.user_id,
                "task_data": log.task_data,
                "timestamp": log.timestamp.isoformat()
            }
            for log in audit_logs
        ]

@app.get("/")
def read_root():
    return {"message": "Audit Service Running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)