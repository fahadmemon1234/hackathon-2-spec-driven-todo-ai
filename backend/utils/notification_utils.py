"""
Utility functions to send notifications based on various events
"""
from sqlmodel import Session
from datetime import datetime, timezone
import sys
import os

# Add the backend directory to the path so we can import from models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import Notification, Task, NotificationType
from schemas.notification import CreateNotificationRequest
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
    task_id: str,
    title: str,
    task=None,
    event_type=None,
    notification_type: str = "task",
    custom_message: str = None
) -> Notification:
    """
    Send a notification about a task event.
    """
    # Use the provided custom message or create a default one
    message = custom_message or f"Task notification for task ID {task_id}"

    # Prepare data dictionary with task info if available
    data = {
        "task_id": task_id,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    if task:
        data.update({
            "task_title": task.title,
            "task_description": task.description,
            "task_priority": task.priority,
            "task_completed": task.completed,
            "task_due_date": task.due_date.isoformat() if task.due_date else None,
        })

    if event_type:
        data["event_type"] = event_type.value if hasattr(event_type, 'value') else event_type

    notification_data = CreateNotificationRequest(
        user_id=user_id,
        title=title,
        message=message,
        type=notification_type.lower(),
        related_task_id=str(task_id),
        data=data
    )

    notification = Notification(
        user_id=notification_data.user_id,
        title=title,
        message=notification_data.message,
        type=notification_type.lower(),
        task_id=task_id,
        related_task_id=notification_data.related_task_id,
        data=notification_data.data
    )

    try:
        session.add(notification)
        # Don't refresh or commit here to avoid interfering with parent transaction
    except Exception as e:
        print(f"Failed to add notification to session: {e}")
        # Don't propagate this error to avoid affecting the main transaction

    return notification


def send_general_notification(
    session: Session,
    user_id: str,
    title: str,
    message: str,
    notification_type: str = "general",
    task_id: int = 1,  # Required for DB constraint
    related_task_id: str = None,
    extra_data: dict = None
) -> Notification:
    """
    Send a general notification to a user.
    """
    notification_data = CreateNotificationRequest(
        user_id=user_id,
        title=title,
        message=message,
        type=notification_type.lower(),
        related_task_id=related_task_id,
        data=extra_data
    )

    notification = Notification(
        user_id=notification_data.user_id,
        title=title,
        message=notification_data.message,
        type=notification_data.type,
        task_id=task_id,
        related_task_id=notification_data.related_task_id,
        data=notification_data.data
    )

    try:
        session.add(notification)
        # Don't refresh or commit here to avoid interfering with parent transaction
    except Exception as e:
        print(f"Failed to add notification to session: {e}")
        # Don't propagate this error to avoid affecting the main transaction

    return notification


def send_system_notification(
    session: Session,
    user_id: str,
    title: str,
    message: str,
    task_id: int = 1
) -> Notification:
    """
    Send a system notification to a user.
    """
    return send_general_notification(
        session=session,
        user_id=user_id,
        title=title,
        message=message,
        notification_type="system",
        task_id=task_id
    )
