from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid
from sqlalchemy import Column, JSON
from enum import Enum


class NotificationType(str, Enum):
    TASK_CREATED = "task_created"
    TASK_UPDATED = "task_updated"
    TASK_COMPLETED = "task_completed"
    TASK_DELETED = "task_deleted"
    REMINDER = "reminder"
    SYSTEM = "system"
    GENERAL = "general"


class NotificationStatus(str, Enum):
    UNREAD = "unread"
    READ = "read"
    ARCHIVED = "archived"


class User(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    email: str = Field(unique=True, index=True)
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # Store Better Auth user UUID as plain string
    user_id: str = Field(
        foreign_key="user.id",
        index=True,
        description="Better Auth user UUID"
    )

    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    priority: str = Field(default="medium", description="high | medium | low | urgent")
    category: Optional[str] = Field(default=None, max_length=50, description="e.g., work, personal, health, shopping")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.utcnow}
    )

    # New fields for Phase 5 - Advanced Features
    tags: List[str] = Field(default=[], sa_column=Column(JSON))
    due_date: Optional[datetime] = Field(default=None)
    is_recurring: bool = Field(default=False)
    recurrence_rule: Optional[str] = Field(default=None, max_length=200, description="RRULE format recurrence pattern")
    next_occurrence: Optional[datetime] = Field(default=None)
    reminder_time: Optional[datetime] = Field(default=None, description="Time to send reminder")
    reminder_type: Optional[str] = Field(default=None, description="Type of reminder: email, push, sms")
    reminder_offset: Optional[int] = Field(default=None, description="Minutes before due date to send reminder")


class Notification(SQLModel, table=True):
    __tablename__ = "notifications"

    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(description="User ID who receives the notification")
    title: str = Field(max_length=200, description="Notification title")
    message: str = Field(max_length=1000, description="Notification message content")
    type: str = Field(default=NotificationType.GENERAL, description="Type of notification")
    status: str = Field(default=NotificationStatus.UNREAD, description="Status of the notification")
    related_task_id: Optional[str] = Field(default=None, description="Related task ID if applicable")
    data: Optional[dict] = Field(default=None, sa_column=Column(JSON), description="Additional data as JSON")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    read_at: Optional[datetime] = Field(default=None, description="Read timestamp")


class ConversationBase(SQLModel):
    user_id: str


class Conversation(ConversationBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to messages
    messages: List["Message"] = Relationship(back_populates="conversation")


class MessageBase(SQLModel):
    conversation_id: int
    role: str
    content: str


class Message(MessageBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id", nullable=False)
    role: str = Field(regex="^(user|assistant)$")  # Using regex to enforce enum-like behavior
    content: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to conversation
    conversation: Conversation = Relationship(back_populates="messages")
