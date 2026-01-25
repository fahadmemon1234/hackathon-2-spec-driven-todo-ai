from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from typing import Optional
import logging
import json
from datetime import datetime
import asyncio
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Notification Service")

class ReminderEvent(BaseModel):
    task_id: int
    user_id: str
    title: str
    due_at: str
    remind_at: str
    type: str = "reminder"
    timestamp: Optional[str] = None

@app.post("/dapr/subscribe/reminders")
async def handle_reminder_subscription(reminder_event: ReminderEvent, background_tasks: BackgroundTasks):
    """
    Dapr subscription endpoint for reminder events.
    This endpoint receives reminder events from the 'reminders' topic.
    """
    logger.info(f"Received reminder event: {reminder_event}")
    
    # Check if remind_at <= current time
    current_time = datetime.utcnow()
    remind_time = datetime.fromisoformat(reminder_event.remind_at.replace('Z', '+00:00'))
    
    if remind_time <= current_time:
        # Schedule notification in background to avoid blocking Dapr
        background_tasks.add_task(send_notification, reminder_event)
        logger.info(f"Scheduled notification for task {reminder_event.task_id}: {reminder_event.title}")
        return {"status": "scheduled"}
    else:
        logger.info(f"Reminder for task {reminder_event.task_id} is in the future, skipping")
        return {"status": "skipped"}

def send_notification(reminder_event: ReminderEvent):
    """
    Send notification to user (console log for now, can be extended to email/push)
    """
    logger.info(f"Sending reminder for task {reminder_event.task_id}: {reminder_event.title}")
    
    # In a real implementation, this would send an actual notification
    # via email, push notification, SMS, etc.
    print(f"NOTIFICATION SENT: Reminder for task {reminder_event.task_id} - {reminder_event.title}")
    print(f"Due at: {reminder_event.due_at}")
    print(f"User ID: {reminder_event.user_id}")
    
    # Placeholder for actual notification logic
    # This could be email, SMS, push notification, etc.

@app.get("/")
def read_root():
    return {"message": "Notification Service Running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)