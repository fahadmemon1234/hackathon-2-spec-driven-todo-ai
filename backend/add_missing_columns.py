"""
Directly add the missing recurrence columns to the task table.
This script bypasses Alembic and directly executes the SQL commands.
"""
import os
from sqlalchemy import create_engine, text

# Get database URL from environment or use default
database_url = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")

# Create engine
engine = create_engine(database_url)

# SQL commands to add missing columns
sql_commands = [
    # Add recurrence_end_date column if it doesn't exist
    """DO $$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                       WHERE table_name = 'task' AND column_name = 'recurrence_end_date') THEN
            ALTER TABLE task ADD COLUMN recurrence_end_date TIMESTAMP;
        END IF;
    END $$;""",
    
    # Add recurrence_max_count column if it doesn't exist
    """DO $$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                       WHERE table_name = 'task' AND column_name = 'recurrence_max_count') THEN
            ALTER TABLE task ADD COLUMN recurrence_max_count INTEGER;
        END IF;
    END $$;""",
    
    # Add original_task_id column if it doesn't exist
    """DO $$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                       WHERE table_name = 'task' AND column_name = 'original_task_id') THEN
            ALTER TABLE task ADD COLUMN original_task_id INTEGER REFERENCES task(id);
        END IF;
    END $$;""",
    
    # Add occurrence_number column if it doesn't exist
    """DO $$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                       WHERE table_name = 'task' AND column_name = 'occurrence_number') THEN
            ALTER TABLE task ADD COLUMN occurrence_number INTEGER DEFAULT 1;
        END IF;
    END $$;""",
    
    # Update occurrence_number to 1 where it's NULL
    "UPDATE task SET occurrence_number = 1 WHERE occurrence_number IS NULL;"
]

# Execute the commands
with engine.connect() as conn:
    trans = conn.begin()
    try:
        for sql_cmd in sql_commands:
            print(f"Executing: {sql_cmd[:50]}...")
            conn.execute(text(sql_cmd))
        trans.commit()
        print("All columns added successfully!")
    except Exception as e:
        trans.rollback()
        print(f"Error executing commands: {e}")
        raise

print("Database schema updated successfully.")