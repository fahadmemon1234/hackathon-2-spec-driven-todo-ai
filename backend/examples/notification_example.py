"""
Example code for using the notification system
"""

from sqlmodel import Session
from datetime import datetime
from db import engine
from models import User, Task
from utils.notification_utils import (
    send_task_notification,
    send_general_notification,
    send_system_notification
)


def create_notification_examples():
    """
    Example of how to create different types of notifications
    """
    # Create a database session
    with Session(engine) as session:
        # Get a user (assuming user exists)
        user = session.exec(User).first()
        if not user:
            print("No users found in the database")
            return

        # Get a task (assuming task exists)
        task = session.exec(Task).first()
        if not task:
            print("No tasks found in the database")
            return

        # Example 1: Send a task-related notification
        print("Sending task-related notification...")
        task_notification = send_task_notification(
            session=session,
            user_id=user.id,
            task=task,
            event_type="task_updated",
            custom_message=f"The task '{task.title}' has been updated with new details."
        )
        print(f"Created task notification: {task_notification.title}")
        
        # Example 2: Send a general notification
        print("\nSending general notification...")
        general_notification = send_general_notification(
            session=session,
            user_id=user.id,
            title="Welcome to Our Platform!",
            message="Thank you for joining our task management platform. We hope you enjoy using our services.",
            notification_type="system",
            extra_data={
                "welcome": True,
                "features": ["tasks", "reminders", "notifications"],
                "timestamp": datetime.utcnow().isoformat()
            }
        )
        print(f"Created general notification: {general_notification.title}")
        
        # Example 3: Send a system notification
        print("\nSending system notification...")
        system_notification = send_system_notification(
            session=session,
            user_id=user.id,
            title="System Maintenance",
            message="Scheduled maintenance will occur tonight from 2 AM to 4 AM EST. Services may be temporarily unavailable."
        )
        print(f"Created system notification: {system_notification.title}")
        
        print("\nNotifications created successfully!")


def api_usage_example():
    """
    Example of how to use the notification API endpoints
    """
    import requests
    import json
    
    # Base API URL
    base_url = "http://localhost:8000/api"
    
    # Example headers (you'd need a valid JWT token)
    headers = {
        "Authorization": "Bearer YOUR_JWT_TOKEN_HERE",  # Replace with actual token
        "Content-Type": "application/json"
    }
    
    # Example 1: Get user's notifications
    print("Example: Get user's notifications")
    print(f"GET {base_url}/notifications/")
    print("Headers:", headers)
    
    # Example 2: Create a notification (internal endpoint, typically called by services)
    print("\nExample: Create a notification")
    create_payload = {
        "user_id": "USER_ID_HERE",  # Replace with actual user ID
        "title": "New Notification",
        "message": "This is a sample notification message",
        "type": "general",
        "related_task_id": "TASK_ID_HERE",  # Optional
        "data": {"key": "value"}  # Optional additional data
    }
    print(f"POST {base_url}/notifications/internal/create")
    print("Payload:", json.dumps(create_payload, indent=2))
    
    # Example 3: Update a notification (mark as read)
    print("\nExample: Update a notification")
    update_payload = {
        "status": "read"
    }
    print(f"PUT {base_url}/notifications/NOTIFICATION_ID_HERE")
    print("Payload:", json.dumps(update_payload, indent=2))
    print("Headers:", headers)
    
    # Example 4: Mark all notifications as read
    print("\nExample: Mark all notifications as read")
    print(f"POST {base_url}/notifications/mark-all-read")
    print("Headers:", headers)
    
    print("\nNote: Replace placeholder values with actual IDs and JWT token to use these endpoints.")


if __name__ == "__main__":
    print("Running notification examples...")
    create_notification_examples()
    print("\n" + "="*50)
    api_usage_example()