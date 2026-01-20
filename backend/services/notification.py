"""
Notification Service

This service consumes reminder events and handles sending notifications
to users when their tasks are due.
"""

import asyncio
import json
import os
from datetime import datetime
from typing import Dict, Any

import sys
import os
# Add the backend directory to the path so we can import from other modules if needed
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

load_dotenv()

app = FastAPI(title="Notification Service")

@app.post("/process_reminder")
async def process_reminder(reminder_data: Dict[Any, Any]):
    """
    Process a reminder event and send notification to the user
    """
    task_id = reminder_data.get("task_id")
    user_id = reminder_data.get("user_id")
    title = reminder_data.get("title")
    due_at = reminder_data.get("due_at")
    remind_at = reminder_data.get("remind_at")
    
    # In a real implementation, this would send an actual notification
    # (email, push notification, SMS, etc.)
    # For this implementation, we'll just log the reminder
    print(f"NOTIFICATION: Reminder for user {user_id} about task '{title}' (ID: {task_id})")
    print(f"Due at: {due_at}, Reminder triggered at: {remind_at}")
    
    # Here you would typically integrate with an actual notification service
    # like SMTP for emails, Firebase for push notifications, etc.
    
    return {
        "message": f"Processed reminder for task {task_id}",
        "user_id": user_id,
        "notification_sent": True
    }


@app.get("/")
def read_root():
    return {"service": "Notification Service", "status": "running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)