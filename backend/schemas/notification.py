from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel


class CreateNotificationRequest(BaseModel):
    user_id: str
    title: str
    message: str
    type: Optional[str] = None
    related_task_id: Optional[str] = None
    data: Optional[Dict[str, Any]] = None


class UpdateNotificationRequest(BaseModel):
    status: Optional[str] = None  # "read", "unread", "archived"


class NotificationResponse(BaseModel):
    id: str
    user_id: str
    title: str
    message: str
    type: str  # Using string instead of enum for flexibility
    status: str  # "unread", "read", "archived"
    related_task_id: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    created_at: datetime
    read_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class NotificationListResponse(BaseModel):
    notifications: list[NotificationResponse]
    total: int
    unread_count: int