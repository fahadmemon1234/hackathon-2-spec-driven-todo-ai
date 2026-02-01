from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime, timezone
import uuid
from sqlalchemy import Column, JSON
from enum import Enum

if TYPE_CHECKING:
    pass


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
    __tablename__ = "user"  # Explicitly set table name
    
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    email: str = Field(index=True, sa_column_kwargs={"unique": True})
    password_hash: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Task(SQLModel, table=True):
    __tablename__ = "task"  # Explicitly set table name
    
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
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)}
    )

    # New fields for Phase 5 - Advanced Features
    tags: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    due_date: Optional[datetime] = Field(default=None)
    is_recurring: bool = Field(default=False)
    recurrence_rule: Optional[str] = Field(default=None, max_length=200, description="RRULE format recurrence pattern")
    next_occurrence: Optional[datetime] = Field(default=None)
    reminder_time: Optional[datetime] = Field(default=None, description="Time to send reminder")
    reminder_type: Optional[str] = Field(default=None, description="Type of reminder: email, push, sms")
    reminder_offset: Optional[int] = Field(default=None, description="Minutes before due date to send reminder")

    # New fields for recurring tasks feature
    recurrence_end_date: Optional[datetime] = Field(default=None, description="Optional end date for recurrence")
    recurrence_max_count: Optional[int] = Field(default=None, description="Maximum number of occurrences")
    original_task_id: Optional[int] = Field(default=None, foreign_key="task.id", description="Reference to original task in recurrence series")
    occurrence_number: Optional[int] = Field(default=1, description="Occurrence number in the recurrence series")

    # Relationship to original task
    original_task: Optional["Task"] = Relationship(
        back_populates="child_tasks",
        sa_relationship_kwargs={
            "primaryjoin": "Task.original_task_id == Task.id",
            "remote_side": "Task.id"
        }
    )

    # Relationship to child tasks
    child_tasks: List["Task"] = Relationship(
        back_populates="original_task",
        sa_relationship_kwargs={
            "primaryjoin": "Task.id == Task.original_task_id",
            "remote_side": "Task.original_task_id"
        }
    )

    @property
    def recurrence_display(self) -> Optional[str]:
        """
        Get a human-readable display text for the recurrence rule.

        Returns:
            Human-readable recurrence description or None if not recurring
        """
        if not self.is_recurring or not self.recurrence_rule:
            return None

        from utils.recurrence_utils import get_recurrence_display_text
        return get_recurrence_display_text(self.recurrence_rule)


class Notification(SQLModel, table=True):
    __tablename__ = "notifications"

    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(description="User ID who receives the notification")
    title: str = Field(max_length=200, description="Notification title")
    message: str = Field(max_length=1000, description="Notification message content")
    type: str = Field(  # maps to DB column 'notification_type'
        default=NotificationType.GENERAL.value,
        sa_column=Column("notification_type", nullable=False)
    )
    status: str = Field(default=NotificationStatus.UNREAD.value)
    related_task_id: Optional[str] = Field(default=None, description="Related task ID if applicable")
    data: Optional[dict] = Field(default=None, sa_column=Column(JSON), description="Additional data as JSON")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Creation timestamp")
    read_at: Optional[datetime] = Field(default=None, description="Read timestamp")


class ConversationBase(SQLModel):
    user_id: str


class Conversation(ConversationBase, table=True):
    __tablename__ = "conversation"  # Explicitly set table name
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id", nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relationship to messages
    messages: List["Message"] = Relationship(back_populates="conversation")


class MessageBase(SQLModel):
    conversation_id: int
    role: str
    content: str


class Message(MessageBase, table=True):
    __tablename__ = "message"  # Explicitly set table name
    
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id", nullable=False)
    role: str = Field(regex="^(user|assistant)$")  # Using regex to enforce enum-like behavior
    content: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relationship to conversation
    conversation: Conversation = Relationship(back_populates="messages")