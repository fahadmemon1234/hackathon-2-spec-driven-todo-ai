"""
Script to fix the notifications table schema in PostgreSQL database
This addresses the "column 'created_at' of relation 'notifications' does not exist" error
"""

import os
from sqlmodel import create_engine
from sqlalchemy import text
from models import SQLModel, Notification
from sqlalchemy.exc import ProgrammingError
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_notifications_schema():
    """
    Add missing columns to the notifications table if they don't exist
    """
    # Get the database URL from environment or use a default
    database_url = os.getenv('DATABASE_URL', '')

    if not database_url or 'dbname' in database_url:
        logger.warning("DATABASE_URL not properly configured, attempting to fix with available connection info")
        # Try to get from config
        try:
            from config import DATABASE_URL as config_db_url
            if config_db_url and 'dbname' not in config_db_url:
                database_url = config_db_url
        except:
            pass

    if not database_url:
        logger.error("No DATABASE_URL found, cannot fix schema")
        return False

    logger.info(f"Connecting to database to fix notifications schema: {database_url}")

    try:
        engine = create_engine(database_url)

        # Check if notifications table exists and get current columns
        with engine.connect() as conn:
            # Get existing columns
            result = conn.execute(text("""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = 'notifications'
            """)).fetchall()

            existing_columns = {row[0] for row in result}
            logger.info(f"Existing columns in notifications table: {existing_columns}")

            # Required columns for Notification model
            required_columns = {
                'id': 'VARCHAR PRIMARY KEY',
                'user_id': 'VARCHAR NOT NULL',
                'title': 'VARCHAR NOT NULL',
                'message': 'VARCHAR NOT NULL',
                'type': 'VARCHAR NOT NULL',
                'status': 'VARCHAR NOT NULL',
                'related_task_id': 'VARCHAR',
                'data': 'JSON',
                'created_at': 'TIMESTAMP WITH TIME ZONE NOT NULL',
                'read_at': 'TIMESTAMP WITH TIME ZONE'
            }

            missing_columns = []
            for col_name in required_columns:
                if col_name not in existing_columns:
                    missing_columns.append(col_name)

            if not missing_columns:
                logger.info("All required columns already exist in notifications table")
                return True

            logger.info(f"Missing columns to add: {missing_columns}")

            # Add missing columns
            with engine.begin() as transaction_conn:
                for col_name in missing_columns:
                    if col_name == 'id':
                        # Special handling for primary key
                        continue
                    elif col_name == 'data':
                        # Handle JSON column
                        alter_sql = f"ALTER TABLE notifications ADD COLUMN {col_name} JSON"
                    elif col_name == 'created_at':
                        # Handle timestamp with timezone
                        alter_sql = f"ALTER TABLE notifications ADD COLUMN {col_name} TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()"
                    else:
                        # Default handling
                        alter_sql = f"ALTER TABLE notifications ADD COLUMN {col_name} {required_columns[col_name].replace('NOT NULL', '').replace('PRIMARY KEY', '').strip()}"

                        # Add NOT NULL constraint if needed, but handle default values
                        if 'NOT NULL' in required_columns[col_name] and 'DEFAULT' not in alter_sql:
                            # For NOT NULL columns, we need to add them as nullable first, then update, then make not null
                            temp_nullable_sql = f"ALTER TABLE notifications ADD COLUMN {col_name}_temp {required_columns[col_name].replace('NOT NULL', '').replace('PRIMARY KEY', '').strip()}"
                            transaction_conn.execute(text(temp_nullable_sql))

                            # Set default values
                            if col_name in ['title', 'message', 'type', 'status']:
                                transaction_conn.execute(text(f"UPDATE notifications SET {col_name}_temp = 'default_{col_name}' WHERE {col_name}_temp IS NULL"))
                            elif col_name == 'user_id':
                                transaction_conn.execute(text(f"UPDATE notifications SET {col_name}_temp = 'default_user' WHERE {col_name}_temp IS NULL"))

                            # Rename the column
                            transaction_conn.execute(text(f"ALTER TABLE notifications RENAME COLUMN {col_name}_temp TO {col_name}"))

                            # Add NOT NULL constraint
                            transaction_conn.execute(text(f"ALTER TABLE notifications ALTER COLUMN {col_name} SET NOT NULL"))
                        else:
                            transaction_conn.execute(text(alter_sql))

                    logger.info(f"Added column: {col_name}")

            logger.info("Successfully added missing columns to notifications table")
            return True

    except ProgrammingError as e:
        if "does not exist" in str(e) and "notifications" in str(e):
            logger.info("Notifications table doesn't exist, creating it with proper schema...")
            # Create the notifications table from scratch
            try:
                SQLModel.metadata.create_all(engine)
                logger.info("Successfully created notifications table with proper schema")
                return True
            except Exception as create_error:
                logger.error(f"Error creating notifications table: {create_error}")
                return False
        else:
            logger.error(f"Programming error: {e}")
            return False
    except Exception as e:
        logger.error(f"Error fixing notifications schema: {e}")
        return False

if __name__ == "__main__":
    success = fix_notifications_schema()
    if success:
        print("SUCCESS: Notifications table schema fixed successfully!")
    else:
        print("FAILED: Failed to fix notifications table schema")
        exit(1)