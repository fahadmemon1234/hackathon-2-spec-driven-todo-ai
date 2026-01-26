"""
Utility functions to send notifications based on various events
"""
from sqlmodel import Session
from datetime import datetime
from models import Notification, User, Task, NotificationType
from schemas.notification import CreateNotificationRequest
from crud.notification import create_notification
from enum import Enum


class NotificationEventType(Enum):
    TASK_CREATED = "task_created"
    TASK_UPDATED = "task_updated"
    TASK_COMPLETED = "task_completed"
    TASK_DELETED = "task_deleted"
    REMINDER = "reminder"


def send_task_notification(
    session: Session,
    user_id: str,
    task: Task,
    event_type: NotificationEventType,
    custom_message: str = None
):
    """
    Send a notification about a task event
    """
    # Define notification titles and messages based on event type
    event_details = {
        NotificationEventType.TASK_CREATED: {
            "title": "New Task Created",
            "message": f"A new task '{task.title}' has been created.",
            "type": "task_created"
        },
        NotificationEventType.TASK_UPDATED: {
            "title": "Task Updated",
            "message": f"The task '{task.title}' has been updated.",
            "type": "task_updated"
        },
        NotificationEventType.TASK_COMPLETED: {
            "title": "Task Completed",
            "message": f"The task '{task.title}' has been marked as completed.",
            "type": "task_completed"
        },
        NotificationEventType.TASK_DELETED: {
            "title": "Task Deleted",
            "message": f"The task '{task.title}' has been deleted.",
            "type": "task_deleted"
        },
        NotificationEventType.REMINDER: {
            "title": "Task Reminder",
            "message": f"Reminder: The task '{task.title}' is due soon.",
            "type": "reminder"
        }
    }
    
    # Get event details or use defaults
    details = event_details.get(event_type, {
        "title": "Task Notification",
        "message": custom_message or f"Task '{task.title}' has been updated.",
        "type": "general"
    })
    
    # Override message if custom message provided
    if custom_message:
        details["message"] = custom_message
    
    # Prepare notification data
    notification_data = CreateNotificationRequest(
        user_id=user_id,
        title=details["title"],
        message=details["message"],
        type=details["type"],
        related_task_id=task.id if hasattr(task, 'id') else None,
        data={
            "task_id": task.id if hasattr(task, 'id') else None,
            "task_title": task.title,
            "event_type": event_type.value,
            "timestamp": datetime.utcnow().isoformat()
        }
    )
    
    # Create the notification
    notification = create_notification(session, notification_data)
    return notification


def send_general_notification(
    session: Session,
    user_id: str,
    title: str,
    message: str,
    notification_type: str = "general",
    related_task_id: str = None,
    extra_data: dict = None
):
    """
    Send a general notification to a user
    """
    notification_data = CreateNotificationRequest(
        user_id=user_id,
        title=title,
        message=message,
        type=notification_type,
        related_task_id=related_task_id,
        data=extra_data
    )
    
    notification = create_notification(session, notification_data)
    return notification


def send_system_notification(
    session: Session,
    user_id: str,
    title: str,
    message: str
):
    """
    Send a system notification to a user
    """
    return send_general_notification(
        session=session,
        user_id=user_id,
        title=title,
        message=message,
        notification_type="system"
    )