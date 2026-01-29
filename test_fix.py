#!/usr/bin/env python3
"""
Test script to verify that the SQLAlchemy duplicate table error is fixed.
This script attempts to import the models and create the database tables.
"""

import sys
import os

# Add the project root to the Python path so we can import from backend
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_imports():
    print("Testing imports...")
    
    # Test importing from backend.models
    from backend.models import User, Task, Conversation, Message, Notification
    print("[OK] Successfully imported User, Task, Conversation, Message, Notification from backend.models")
    
    # Test importing from routes that were problematic
    from backend.routes.auth import UserCreate, UserLogin
    print("[OK] Successfully imported UserCreate, UserLogin from backend.routes.auth")
    
    # Test importing from db
    from backend.db import engine
    print("[OK] Successfully imported engine from backend.db")
    
    # Test importing from db
    from backend.db import create_db_and_tables
    print("[OK] Successfully imported create_db_and_tables from backend.db")
    
    print("\nAll imports successful! Testing table creation...")
    
    # Try to create the tables (this was failing before)
    try:
        create_db_and_tables()
        print("[OK] Successfully created database tables without errors!")
    except Exception as e:
        print(f"[ERROR] Error creating tables: {e}")
        raise
    
    print("\n[SUCCESS] All tests passed! The duplicate table error has been fixed.")
    

if __name__ == "__main__":
    test_imports()