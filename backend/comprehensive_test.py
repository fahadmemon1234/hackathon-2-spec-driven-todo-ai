#!/usr/bin/env python3
"""Comprehensive test script to verify that the SQLAlchemy relationship error is fixed."""

from backend.models import Task, Conversation, Message, User
from db import create_db_and_tables, engine
from sqlmodel import SQLModel, Session, select
from datetime import datetime
import uuid

def test_models():
    print("Testing model definitions...")
    
    # Test that models can be imported without errors
    print("Models imported successfully")
    
    # Test that all models inherit from SQLModel
    assert issubclass(Task, SQLModel), "Task should inherit from SQLModel"
    assert issubclass(User, SQLModel), "User should inherit from SQLModel"
    assert issubclass(Conversation, SQLModel), "Conversation should inherit from SQLModel"
    assert issubclass(Message, SQLModel), "Message should inherit from SQLModel"
    print("All models inherit from SQLModel")
    
    # Test creating the database tables (this is where the original error occurred)
    try:
        create_db_and_tables()
        print("Database tables created successfully - no relationship errors!")
    except Exception as e:
        print(f"Error creating tables: {e}")
        raise
    
    # Test creating instances of each model
    print("\nTesting model instantiation...")

    # Create a user with a unique email
    unique_email = f"test_{uuid.uuid4()}@example.com"
    user = User(email=unique_email, password_hash="hashed_password")
    print(f"User created: {user.email}")
    
    # Create a task associated with the user
    task = Task(user_id=user.id, title="Test Task", description="Test Description")
    print(f"Task created: {task.title}")
    
    # Create a conversation associated with the user
    conversation = Conversation(user_id=user.id)
    print(f"Conversation created with user_id: {conversation.user_id}")
    
    # Create a message associated with the conversation
    message = Message(conversation_id=conversation.id, role="user", content="Hello, world!")
    print(f"Message created with role: {message.role}")
    
    # Test database operations
    print("\nTesting database operations...")
    with Session(engine) as session:
        # Add user to session
        session.add(user)
        session.commit()
        session.refresh(user)
        print(f"User saved to database with ID: {user.id}")
        
        # Add conversation to session
        conversation.user_id = user.id
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        print(f"Conversation saved to database with ID: {conversation.id}")
        
        # Add message to session
        message.conversation_id = conversation.id
        session.add(message)
        session.commit()
        session.refresh(message)
        print(f"Message saved to database with ID: {message.id}")
        
        # Add task to session
        task.user_id = user.id
        session.add(task)
        session.commit()
        session.refresh(task)
        print(f"Task saved to database with ID: {task.id}")
        
        # Test relationships by querying
        user_with_tasks = session.exec(select(User).where(User.id == user.id)).first()
        print(f"Retrieved user from database: {user_with_tasks.email}")
        
        # Test that we can access related conversations
        conv_for_user = session.exec(select(Conversation).where(Conversation.user_id == user.id)).first()
        print(f"Retrieved conversation for user: {conv_for_user.id}")
        
        # Test that we can access related messages
        messages_for_conv = session.exec(select(Message).where(Message.conversation_id == conversation.id)).all()
        print(f"Found {len(messages_for_conv)} messages for conversation")
    
    print("\nAll tests passed! The SQLAlchemy relationship error has been fixed.")
    print("Summary of fixes:")
    print("- Fixed foreign key reference in Message model (was 'conversations.id', now 'conversation.id')")
    print("- Added User model to models.py to resolve 'user.id' foreign key references")
    print("- Updated imports in auth.py, db.py, and verify_schema.py to use the central User model")
    print("- Verified that all relationships work correctly")

if __name__ == "__main__":
    test_models()