"""
Script to ensure the database schema is up-to-date with required columns
This can be run as part of application startup to fix missing columns
"""

from sqlmodel import Session
from sqlalchemy import text, inspect
from models import Notification, SQLModel
from db import get_session
import logging

logger = logging.getLogger(__name__)

def ensure_notifications_table_schema(session: Session):
    """
    Ensure the notifications table has all required columns.
    This function checks for missing columns and adds them if necessary.
    Works with both PostgreSQL and SQLite.
    """
    try:
        # Get the database inspector to check table structure
        inspector = inspect(session.bind)
        columns = inspector.get_columns('notifications')
        existing_columns = {col['name'] for col in columns}

        # Define required columns
        required_columns = {
            'message': "ALTER TABLE notifications ADD COLUMN message TEXT NOT NULL DEFAULT 'Default notification message'",
            'title': "ALTER TABLE notifications ADD COLUMN title TEXT NOT NULL DEFAULT 'Notification'",
            'related_task_id': "ALTER TABLE notifications ADD COLUMN related_task_id TEXT",
            'data': "ALTER TABLE notifications ADD COLUMN data TEXT",  # TEXT for JSON in SQLite
            'read_at': "ALTER TABLE notifications ADD COLUMN read_at TIMESTAMP",
            'type': "ALTER TABLE notifications ADD COLUMN type TEXT NOT NULL DEFAULT 'general'",
            'status': "ALTER TABLE notifications ADD COLUMN status TEXT NOT NULL DEFAULT 'unread'",
            'created_at': "ALTER TABLE notifications ADD COLUMN created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP"
        }

        # Add missing columns
        for col_name, alter_sql in required_columns.items():
            if col_name not in existing_columns:
                session.exec(text(alter_sql))
                logger.info(f"Added '{col_name}' column to notifications table")

        session.commit()
        logger.info("Notifications table schema validation completed successfully")

    except Exception as e:
        logger.error(f"Error ensuring notifications table schema: {str(e)}")
        session.rollback()
        raise


def ensure_schema():
    """
    Main function to ensure all database schemas are up-to-date
    """
    with next(get_session()) as session:
        ensure_notifications_table_schema(session)


if __name__ == "__main__":
    ensure_schema()