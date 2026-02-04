"""
Direct database schema update script for reminder fields
This script adds the reminder fields directly to the database if they don't exist
"""
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")

# Create database engine
engine = create_engine(DATABASE_URL)

def add_reminder_fields():
    """
    Add reminder fields to the task table if they don't exist
    """
    with engine.connect() as conn:
        # Check if reminder_time column exists
        result = conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'task' AND column_name = 'reminder_time'
        """))
        if not result.fetchone():
            print("Adding reminder_time column...")
            conn.execute(text("ALTER TABLE task ADD COLUMN reminder_time TIMESTAMP WITH TIME ZONE"))
            conn.commit()
            print("reminder_time column added successfully")
        else:
            print("reminder_time column already exists")

        # Check if reminder_type column exists
        result = conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'task' AND column_name = 'reminder_type'
        """))
        if not result.fetchone():
            print("Adding reminder_type column...")
            conn.execute(text("ALTER TABLE task ADD COLUMN reminder_type VARCHAR(50)"))
            conn.commit()
            print("reminder_type column added successfully")
        else:
            print("reminder_type column already exists")

        # Check if reminder_offset column exists
        result = conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'task' AND column_name = 'reminder_offset'
        """))
        if not result.fetchone():
            print("Adding reminder_offset column...")
            conn.execute(text("ALTER TABLE task ADD COLUMN reminder_offset INTEGER"))
            conn.commit()
            print("reminder_offset column added successfully")
        else:
            print("reminder_offset column already exists")

    print("All reminder fields have been added to the database!")

if __name__ == "__main__":
    add_reminder_fields()