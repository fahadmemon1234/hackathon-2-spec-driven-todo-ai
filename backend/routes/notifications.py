from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import Optional
from dependencies import get_current_user_id
from db import get_session
from models import NotificationType
from schemas.notification import (
    CreateNotificationRequest,
    UpdateNotificationRequest,
    NotificationListResponse,
    NotificationResponse
)
from crud.notification import (
    create_notification,
    get_notifications_by_user,
    get_notification_by_id,
    update_notification,
    mark_all_as_read,
    delete_notification
)

router = APIRouter(prefix="/notifications")


@router.get("/", response_model=NotificationListResponse)
def list_notifications(
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 20,
    status: Optional[str] = None
):
    """
    Get notifications for the current user
    """
    notifications, total, unread_count = get_notifications_by_user(
        session, user_id, skip, limit, status
    )
    
    return NotificationListResponse(
        notifications=notifications,
        total=total,
        unread_count=unread_count
    )


@router.post("/", response_model=NotificationResponse)
def create_notification_endpoint(
    notification_data: CreateNotificationRequest,
    session: Session = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Create a new notification
    NOTE: Only the user themselves can create a notification for themselves
    In a real system, this would be called internally by other services
    """
    # For security, ensure the user can only create notifications for themselves
    if notification_data.user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not authorized to create notification for this user")
    
    notification = create_notification(session, notification_data)
    return notification


@router.get("/{notification_id}", response_model=NotificationResponse)
def get_notification(
    notification_id: str,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Get a specific notification
    """
    notification = get_notification_by_id(session, notification_id, user_id)
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    return notification


@router.put("/{notification_id}", response_model=NotificationResponse)
def update_notification_endpoint(
    notification_id: str,
    update_data: UpdateNotificationRequest,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Update a notification (currently only supports changing status)
    """
    updated_notification = update_notification(
        session, notification_id, user_id, update_data
    )
    
    if not updated_notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    return updated_notification


@router.delete("/{notification_id}", status_code=204)
def delete_notification_endpoint(
    notification_id: str,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Delete a notification
    """
    success = delete_notification(session, notification_id, user_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    return {"detail": "Notification deleted successfully"}


@router.post("/mark-all-read", status_code=200)
def mark_all_notifications_as_read(
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Mark all notifications as read for the current user
    """
    updated_count = mark_all_as_read(session, user_id)
    return {"detail": f"Marked {updated_count} notifications as read"}


# Internal endpoint for services to create notifications for users
@router.post("/internal/create", response_model=NotificationResponse)
def create_internal_notification(
    notification_data: CreateNotificationRequest,
    session: Session = Depends(get_session)
):
    """
    Internal endpoint for services to create notifications
    This would typically be protected by internal authentication
    """
    # In a real system, this would be secured differently
    # For now, we'll allow it but in production you'd want to verify the caller
    notification = create_notification(session, notification_data)
    return notification