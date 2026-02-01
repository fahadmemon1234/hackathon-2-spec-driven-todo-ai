"""
Test script to verify reminder functionality
"""

import sys
import os
# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import asyncio
from datetime import datetime, timedelta, timezone
from sqlmodel import create_engine, Session, select
from models import Task
from services.reminder_scheduler import ReminderScheduler
from utils.event_publisher import EventPublisher


def test_reminder_functionality():
    """
    Test the reminder functionality
    """
    print("Testing reminder functionality...")
    
    # Create a sample task with a due date
    task = Task(
        user_id="test_user_123",
        title="Test Task with Reminder",
        description="This is a test task to verify reminder functionality",
        priority="medium",
        due_date=datetime.now(timezone.utc) + timedelta(minutes=5),  # Due in 5 minutes
        reminder_offset=2,  # Send reminder 2 minutes before due
        reminder_type="BEFORE_DUE"
    )
    
    print(f"Created test task: {task.title}")
    print(f"Due date: {task.due_date}")
    print(f"Reminder offset: {task.reminder_offset} minutes")
    
    # Initialize the reminder scheduler
    scheduler = ReminderScheduler()
    
    # Schedule a reminder for the task
    success = scheduler.schedule_reminder_for_task(task)
    
    if success:
        print("[SUCCESS] Reminder scheduled successfully!")
    else:
        print("[FAILED] Failed to schedule reminder")
    
    # Test checking for due reminders
    sent_count = scheduler.check_and_send_due_reminders()
    print(f"Checked for due reminders, would have sent: {sent_count}")
    
    # Cleanup
    scheduler.close()
    

if __name__ == "__main__":
    test_reminder_functionality()