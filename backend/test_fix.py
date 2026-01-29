#!/usr/bin/env python3
"""
Test script to verify that the SQLAlchemy duplicate table error is fixed.
This script attempts to import the models and create the database tables.
"""

def test_imports():
    print("Testing imports...")
    
    # Test importing from backend.models
    from backend.models import User, Task, Conversation, Message, Notification
    print("✓ Successfully imported User, Task, Conversation, Message, Notification from backend.models")
    
    # Test importing from routes that were problematic
    from backend.routes.auth import UserCreate, UserLogin
    print("✓ Successfully imported UserCreate, UserLogin from backend.routes.auth")
    
    # Test importing from db
    from backend.db import engine
    print("✓ Successfully imported engine from backend.db")
    
    # Test creating tables (this is where the original error occurred)
    from backend.db import create_db_and_tables
    print("✓ Successfully imported create_db_and_tables from backend.db")
    
    print("\nAll imports successful! Testing table creation...")
    
    # Try to create the tables (this was failing before)
    try:
        create_db_and_tables()
        print("✓ Successfully created database tables without errors!")
    except Exception as e:
        print(f"✗ Error creating tables: {e}")
        raise
    
    print("\n🎉 All tests passed! The duplicate table error has been fixed.")
    

if __name__ == "__main__":
    test_imports()