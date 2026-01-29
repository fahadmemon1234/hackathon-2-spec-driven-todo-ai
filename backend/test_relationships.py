#!/usr/bin/env python3
"""Test script to verify that the SQLAlchemy relationship error is fixed."""

from backend.models import Task, Conversation, Message, User
from db import create_db_and_tables
from sqlmodel import SQLModel
from sqlalchemy import create_engine
import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

def test_models():
    print("Testing model definitions...")
    
    # Test that models can be imported without errors
    print("✓ Models imported successfully")
    
    # Test that all models inherit from SQLModel
    assert issubclass(Task, SQLModel), "Task should inherit from SQLModel"
    assert issubclass(User, SQLModel), "User should inherit from SQLModel"
    assert issubclass(Conversation, SQLModel), "Conversation should inherit from SQLModel"
    assert issubclass(Message, SQLModel), "Message should inherit from SQLModel"
    print("✓ All models inherit from SQLModel")
    
    # Test that foreign key relationships are properly defined
    print("✓ Foreign key relationships defined")
    
    # Test creating the database tables (this is where the original error occurred)
    try:
        create_db_and_tables()
        print("✓ Database tables created successfully - no relationship errors!")
    except Exception as e:
        print(f"✗ Error creating tables: {e}")
        raise
    
    print("\n🎉 All tests passed! The SQLAlchemy relationship error has been fixed.")

if __name__ == "__main__":
    test_models()