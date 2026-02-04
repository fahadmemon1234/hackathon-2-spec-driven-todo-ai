"""
Direct database schema update script for notifications table
This script adds the missing columns to the notifications table if they don't exist
"""
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/todo_db")

# Create database engine
engine = create_engine(DATABASE_URL)

def add_missing_notification_columns():
    """
    Add missing columns to the notifications table if they don't exist
    """
    with engine.connect() as conn:
        # Check if title column exists
        result = conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'notifications' AND column_name = 'title'
        """))
        if not result.fetchone():
            print("Adding title column to notifications table...")
            conn.execute(text("ALTER TABLE notifications ADD COLUMN title VARCHAR(200)"))
            conn.commit()
            print("Title column added successfully")
        else:
            print("Title column already exists")

        # Check if related_task_id column exists
        result = conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'notifications' AND column_name = 'related_task_id'
        """))
        if not result.fetchone():
            print("Adding related_task_id column to notifications table...")
            conn.execute(text("ALTER TABLE notifications ADD COLUMN related_task_id VARCHAR(255)"))
            conn.commit()
            print("Related_task_id column added successfully")
        else:
            print("Related_task_id column already exists")

        # Check if data column exists
        result = conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'notifications' AND column_name = 'data'
        """))
        if not result.fetchone():
            print("Adding data column to notifications table...")
            conn.execute(text("ALTER TABLE notifications ADD COLUMN data JSON"))
            conn.commit()
            print("Data column added successfully")
        else:
            print("Data column already exists")

        # Check if read_at column exists
        result = conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'notifications' AND column_name = 'read_at'
        """))
        if not result.fetchone():
            print("Adding read_at column to notifications table...")
            conn.execute(text("ALTER TABLE notifications ADD COLUMN read_at TIMESTAMP WITH TIME ZONE"))
            conn.commit()
            print("Read_at column added successfully")
        else:
            print("Read_at column already exists")

        # Check if status column exists
        result = conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'notifications' AND column_name = 'status'
        """))
        if not result.fetchone():
            print("Adding status column to notifications table...")
            conn.execute(text("ALTER TABLE notifications ADD COLUMN status VARCHAR(20) DEFAULT 'unread'"))
            conn.commit()
            print("Status column added successfully")
        else:
            print("Status column already exists")

    print("All missing notification columns have been added to the database!")

if __name__ == "__main__":
    add_missing_notification_columns()