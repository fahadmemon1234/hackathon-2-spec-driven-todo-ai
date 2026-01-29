from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, validator, Field
from enum import Enum
import re


class ReminderType(str, Enum):
    EMAIL = "email"
    PUSH = "push"
    SMS = "sms"
    BEFORE_DUE = "before_due"


class PriorityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class CreateTaskRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    priority: Optional[PriorityLevel] = "medium"
    category: Optional[str] = Field(None, max_length=50)
    tags: Optional[List[str]] = []
    due_date: Optional[datetime] = None
    is_recurring: Optional[bool] = False
    recurrence_rule: Optional[str] = Field(None, max_length=200)
    recurrence_end_date: Optional[datetime] = None
    recurrence_max_count: Optional[int] = Field(None, ge=1)  # Greater than or equal to 1
    original_task_id: Optional[int] = None
    occurrence_number: Optional[int] = Field(1, ge=1)  # Greater than or equal to 1
    reminder_time: Optional[datetime] = None
    reminder_type: Optional[ReminderType] = None
    reminder_offset: Optional[int] = None

    @validator('title')
    def validate_title(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Title cannot be empty')
        return v.strip()

    @validator('due_date', 'recurrence_end_date', 'reminder_time')
    def validate_datetime(cls, v):
        if v and v < datetime.now():
            raise ValueError('Date/time cannot be in the past')
        return v

    @validator('recurrence_rule')
    def validate_recurrence_rule(cls, v):
        if v is not None and v.strip():
            # Basic validation for RRULE format - check if it has FREQ component
            if 'FREQ=' not in v.upper():
                raise ValueError('Recurrence rule must contain FREQ component')
            
            # Additional validation could be added here for more complex RRULE validation
            # For now, we'll just check the basic format
            if not re.match(r'^([A-Z]+=([A-Z0-9]+;?)+)+$', v.upper()):
                # This is a simplified validation - in production, you might want to use a more robust RRULE validator
                pass  # For now, let's just accept the format as is and validate during processing
        
        return v

    @validator('recurrence_max_count')
    def validate_recurrence_max_count(cls, v):
        if v is not None and v < 1:
            raise ValueError('Recurrence max count must be at least 1')
        return v

    @validator('occurrence_number')
    def validate_occurrence_number(cls, v):
        if v is not None and v < 1:
            raise ValueError('Occurrence number must be at least 1')
        return v

    @validator('reminder_offset')
    def validate_reminder_offset(cls, v):
        if v is not None and v < 0:
            raise ValueError('Reminder offset cannot be negative')
        return v

    @validator('original_task_id')
    def validate_original_task_id(cls, v):
        if v is not None and v < 1:
            raise ValueError('Original task ID must be a positive integer')
        return v


class UpdateTaskRequest(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[PriorityLevel] = None
    category: Optional[str] = Field(None, max_length=50)
    tags: Optional[List[str]] = None
    due_date: Optional[datetime] = None
    is_recurring: Optional[bool] = None
    recurrence_rule: Optional[str] = Field(None, max_length=200)
    recurrence_end_date: Optional[datetime] = None
    recurrence_max_count: Optional[int] = Field(None, ge=1)  # Greater than or equal to 1
    original_task_id: Optional[int] = None
    occurrence_number: Optional[int] = Field(None, ge=1)  # Greater than or equal to 1
    reminder_time: Optional[datetime] = None
    reminder_type: Optional[ReminderType] = None
    reminder_offset: Optional[int] = None

    @validator('due_date', 'recurrence_end_date', 'reminder_time')
    def validate_datetime(cls, v):
        if v and v < datetime.now():
            raise ValueError('Date/time cannot be in the past')
        return v

    @validator('recurrence_rule')
    def validate_recurrence_rule(cls, v):
        if v is not None and v.strip():
            # Basic validation for RRULE format - check if it has FREQ component
            if 'FREQ=' not in v.upper():
                raise ValueError('Recurrence rule must contain FREQ component')
        return v

    @validator('recurrence_max_count')
    def validate_recurrence_max_count(cls, v):
        if v is not None and v < 1:
            raise ValueError('Recurrence max count must be at least 1')
        return v

    @validator('occurrence_number')
    def validate_occurrence_number(cls, v):
        if v is not None and v < 1:
            raise ValueError('Occurrence number must be at least 1')
        return v

    @validator('reminder_offset')
    def validate_reminder_offset(cls, v):
        if v is not None and v < 0:
            raise ValueError('Reminder offset cannot be negative')
        return v

    @validator('original_task_id')
    def validate_original_task_id(cls, v):
        if v is not None and v < 1:
            raise ValueError('Original task ID must be a positive integer')
        return v


class TaskResponse(BaseModel):
    id: int
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
    recurrence_display: Optional[str] = None  # Human-readable recurrence description
    recurrence_end_date: Optional[datetime] = None
    recurrence_max_count: Optional[int] = None
    original_task_id: Optional[int] = None
    occurrence_number: Optional[int] = 1
    next_occurrence: Optional[datetime] = None
    reminder_time: Optional[datetime] = None
    reminder_type: Optional[ReminderType] = None
    reminder_offset: Optional[int] = None

    class Config:
        from_attributes = True