from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, validator
from enum import Enum


class ReminderType(str, Enum):
    EMAIL = "email"
    PUSH = "push"
    SMS = "sms"


class PriorityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class UpdateTaskRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[PriorityLevel] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    due_date: Optional[datetime] = None
    is_recurring: Optional[bool] = None
    recurrence_rule: Optional[str] = None
    reminder_time: Optional[datetime] = None
    reminder_type: Optional[ReminderType] = None
    reminder_offset: Optional[int] = None

    @validator('due_date', 'reminder_time')
    def validate_datetime(cls, v):
        if v and v < datetime.now():
            raise ValueError('Date/time cannot be in the past')
        return v

    @validator('reminder_offset')
    def validate_reminder_offset(cls, v):
        if v is not None and v < 0:
            raise ValueError('Reminder offset cannot be negative')
        return v


class TaskResponse(BaseModel):
    id: str
    user_id: str
    title: str
    description: Optional[str] = None
    completed: bool
    created_at: datetime
    updated_at: datetime
    priority: Optional[PriorityLevel] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    due_date: Optional[datetime] = None
    is_recurring: bool
    recurrence_rule: Optional[str] = None
    next_occurrence: Optional[datetime] = None
    reminder_time: Optional[datetime] = None
    reminder_type: Optional[ReminderType] = None
    reminder_offset: Optional[int] = None

    class Config:
        from_attributes = True