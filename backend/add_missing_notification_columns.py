import os
from sqlalchemy import create_engine, text
import traceback

# Get database URL from environment or use default
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/dbname')
print(f"Attempting to connect to database: {DATABASE_URL}")

try:
    engine = create_engine(DATABASE_URL)
    
    # Add the missing message column to the notifications table
    with engine.connect() as conn:
        trans = conn.begin()
        try:
            # Check if the message column exists
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'notifications' AND column_name = 'message'
            """))
            
            if not result.fetchone():
                # Add the message column
                conn.execute(text("""
                    ALTER TABLE notifications ADD COLUMN message TEXT NOT NULL DEFAULT 'Default notification message'
                """))
                print('Added message column to notifications table')
            else:
                print('Message column already exists')
                
            # Also make sure other required columns exist
            # Check for title column
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'notifications' AND column_name = 'title'
            """))
            
            if not result.fetchone():
                conn.execute(text("""
                    ALTER TABLE notifications ADD COLUMN title VARCHAR(200) NOT NULL DEFAULT 'Notification'
                """))
                print('Added title column to notifications table')
            
            trans.commit()
            print('Successfully updated notifications table schema')
        except Exception as e:
            trans.rollback()
            print(f'Error updating notifications table: {e}')
            traceback.print_exc()
except Exception as e:
    print(f"Error connecting to database: {e}")
    traceback.print_exc()