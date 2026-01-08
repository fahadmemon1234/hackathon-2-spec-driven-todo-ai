# Data Model Design: AI-Powered Chatbot for Task Management

**Feature**: 14-ai-chatbot-task-management
**Created**: 2026-01-06
**Status**: Completed

## Entity Definitions

### Conversation
Represents a single chat session between user and AI, containing metadata like creation time and user ID.

- **id**: integer (primary key, auto-increment)
- **user_id**: string (foreign key to users table, enforces ownership)
- **created_at**: datetime (timestamp when conversation started, defaults to current time)
- **updated_at**: datetime (timestamp of last activity, updates automatically)

**Validation Rules**:
- user_id must correspond to an existing user in the system
- created_at and updated_at are automatically managed by the system

**State Transitions**:
- Created when a new conversation is initiated
- Updated when new messages are added to the conversation

### Message
Represents individual messages in a conversation, with role (user/assistant) and content.

- **id**: integer (primary key, auto-increment)
- **conversation_id**: integer (foreign key to conversations table, cascading delete)
- **role**: string (enum: "user" | "assistant", determines message origin)
- **content**: text (the actual message content, required)
- **created_at**: datetime (timestamp when message was created, defaults to current time)

**Validation Rules**:
- conversation_id must correspond to an existing conversation
- role must be either "user" or "assistant"
- content cannot be empty or null
- created_at is automatically managed by the system

**State Transitions**:
- Created when a new message is added to a conversation
- Immutable after creation (messages cannot be modified, only added)

### Relationship Diagram
```
User (1) → Conversations (Many)
Conversation (1) → Messages (Many)
```

## Database Schema

### conversations table
```sql
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user_id TEXT REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### messages table
```sql
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER REFERENCES conversations(id) ON DELETE CASCADE,
    role TEXT CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Indexes
```sql
CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
```

## SQLModel Class Definitions

### Conversation Model
```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
import datetime

class ConversationBase(SQLModel):
    user_id: str

class Conversation(ConversationBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", nullable=False)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    
    # Relationship to messages
    messages: list["Message"] = Relationship(back_populates="conversation")
```

### Message Model
```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
import datetime

class MessageBase(SQLModel):
    conversation_id: int
    role: str
    content: str

class Message(MessageBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", nullable=False)
    role: str = Field(regex="^(user|assistant)$")  # Using regex to enforce enum-like behavior
    content: str = Field(nullable=False)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    
    # Relationship to conversation
    conversation: Conversation = Relationship(back_populates="messages")
```

## Validation Rules from Requirements

### Conversation Validation
- **FR-003**: System MUST maintain conversation history in database
  - Implemented through the Conversation model with timestamps
- **FR-004**: System MUST authenticate users via JWT tokens
  - Enforced through user_id foreign key relationship
- **FR-005**: System MUST enforce user ownership of tasks
  - Achieved through user_id foreign key ensuring conversations belong to specific users

### Message Validation
- **FR-001**: System MUST provide chat interface for task management
  - Implemented through Message model storing user and assistant interactions
- **FR-003**: System MUST maintain conversation history
  - Achieved through Conversation-Messages relationship
- **FR-006**: System MUST provide friendly, human-like responses
  - Role field distinguishes between user inputs and assistant responses