from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

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
    priority: str = Field(default="medium", description="high | medium | low")
    category: Optional[str] = Field(default=None, max_length=50, description="e.g., work, personal, health, shopping")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.utcnow}
    )
