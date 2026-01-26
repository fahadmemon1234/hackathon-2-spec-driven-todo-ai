from typing import List, Optional
from sqlmodel import Session, select, func
from models import Notification, NotificationStatus
from schemas.notification import CreateNotificationRequest, UpdateNotificationRequest


def create_notification(session: Session, notification_data: CreateNotificationRequest) -> Notification:
    """
    Create a new notification
    """
    notification = Notification(
        user_id=notification_data.user_id,
        title=notification_data.title,
        message=notification_data.message,
        type=notification_data.type or "general",
        related_task_id=notification_data.related_task_id,
        data=notification_data.data
    )
    
    session.add(notification)
    session.commit()
    session.refresh(notification)
    
    return notification


def get_notifications_by_user(
    session: Session, 
    user_id: str, 
    skip: int = 0, 
    limit: int = 20,
    status: Optional[str] = None
) -> tuple[List[Notification], int, int]:
    """
    Get notifications for a specific user with pagination and optional status filter
    Returns (notifications, total_count, unread_count)
    """
    # Base query for user's notifications
    query = select(Notification).where(Notification.user_id == user_id)
    
    # Apply status filter if provided
    if status:
        query = query.where(Notification.status == status)
    
    # Get total count
    total_query = select(func.count(Notification.id)).where(Notification.user_id == user_id)
    if status:
        total_query = total_query.where(Notification.status == status)
    total_count = session.exec(total_query).one()
    
    # Get unread count
    unread_query = select(func.count(Notification.id)).where(
        Notification.user_id == user_id,
        Notification.status == NotificationStatus.UNREAD
    )
    unread_count = session.exec(unread_query).one()
    
    # Apply pagination and ordering
    query = query.offset(skip).limit(limit).order_by(Notification.created_at.desc())
    notifications = session.exec(query).all()
    
    return notifications, total_count, unread_count


def get_notification_by_id(session: Session, notification_id: str, user_id: str) -> Optional[Notification]:
    """
    Get a specific notification by ID for a user
    """
    query = select(Notification).where(
        Notification.id == notification_id,
        Notification.user_id == user_id
    )
    return session.exec(query).first()


def update_notification(
    session: Session, 
    notification_id: str, 
    user_id: str, 
    update_data: UpdateNotificationRequest
) -> Optional[Notification]:
    """
    Update a notification's status
    """
    notification = get_notification_by_id(session, notification_id, user_id)
    
    if not notification:
        return None
    
    # Update status if provided
    if update_data.status:
        notification.status = update_data.status
        if update_data.status == "read" and not notification.read_at:
            from datetime import datetime
            notification.read_at = datetime.utcnow()
    
    session.add(notification)
    session.commit()
    session.refresh(notification)
    
    return notification


def mark_all_as_read(session: Session, user_id: str) -> int:
    """
    Mark all notifications as read for a user
    Returns the number of notifications updated
    """
    from datetime import datetime
    from sqlmodel import and_
    
    # Find all unread notifications for the user
    notifications = session.exec(
        select(Notification).where(
            and_(
                Notification.user_id == user_id,
                Notification.status == NotificationStatus.UNREAD
            )
        )
    ).all()
    
    updated_count = 0
    for notification in notifications:
        notification.status = NotificationStatus.READ
        notification.read_at = datetime.utcnow()
        session.add(notification)
        updated_count += 1
    
    session.commit()
    return updated_count


def delete_notification(session: Session, notification_id: str, user_id: str) -> bool:
    """
    Delete a notification
    """
    notification = get_notification_by_id(session, notification_id, user_id)
    
    if not notification:
        return False
    
    session.delete(notification)
    session.commit()
    return True