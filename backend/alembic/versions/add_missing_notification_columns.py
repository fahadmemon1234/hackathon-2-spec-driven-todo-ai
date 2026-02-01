"""Add missing columns to notifications table if they don't exist

Revision ID: add_missing_notification_columns
Revises: add_notification_title_column
Create Date: 2026-01-31 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'add_missing_notification_columns'
down_revision = 'add_notification_title_column'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Get the connection
    conn = op.get_bind()
    
    # Check if 'message' column exists, add it if not
    message_col_exists = conn.execute(
        sa.text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='notifications' AND column_name='message'
        """)
    ).fetchone()
    
    if not message_col_exists:
        op.add_column('notifications', sa.Column('message', sa.String(length=1000), nullable=True))
        # Set a default value for existing rows
        op.execute("UPDATE notifications SET message = 'Default notification message' WHERE message IS NULL")
        # Make the column non-nullable
        op.alter_column('notifications', 'message', nullable=False)
        print("Added 'message' column to notifications table")
    
    # Check if 'title' column exists, add it if not
    title_col_exists = conn.execute(
        sa.text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='notifications' AND column_name='title'
        """)
    ).fetchone()
    
    if not title_col_exists:
        op.add_column('notifications', sa.Column('title', sa.String(length=200), nullable=True))
        op.execute("UPDATE notifications SET title = 'Notification' WHERE title IS NULL")
        op.alter_column('notifications', 'title', nullable=False)
        print("Added 'title' column to notifications table")
    
    # Check if 'related_task_id' column exists, add it if not
    related_task_id_col_exists = conn.execute(
        sa.text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='notifications' AND column_name='related_task_id'
        """)
    ).fetchone()
    
    if not related_task_id_col_exists:
        op.add_column('notifications', sa.Column('related_task_id', sa.String(), nullable=True))
        print("Added 'related_task_id' column to notifications table")
    
    # Check if 'data' column exists, add it if not
    data_col_exists = conn.execute(
        sa.text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='notifications' AND column_name='data'
        """)
    ).fetchone()
    
    if not data_col_exists:
        op.add_column('notifications', sa.Column('data', postgresql.JSON, nullable=True))
        print("Added 'data' column to notifications table")
    
    # Check if 'read_at' column exists, add it if not
    read_at_col_exists = conn.execute(
        sa.text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='notifications' AND column_name='read_at'
        """)
    ).fetchone()
    
    if not read_at_col_exists:
        op.add_column('notifications', sa.Column('read_at', sa.DateTime(), nullable=True))
        print("Added 'read_at' column to notifications table")


def downgrade() -> None:
    # Remove the columns if they exist
    conn = op.get_bind()
    
    # Check and drop 'message' column if it exists
    message_col_exists = conn.execute(
        sa.text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='notifications' AND column_name='message'
        """)
    ).fetchone()
    
    if message_col_exists:
        op.drop_column('notifications', 'message')
        print("Removed 'message' column from notifications table")
    
    # Check and drop 'title' column if it exists
    title_col_exists = conn.execute(
        sa.text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='notifications' AND column_name='title'
        """)
    ).fetchone()
    
    if title_col_exists:
        op.drop_column('notifications', 'title')
        print("Removed 'title' column from notifications table")
    
    # Check and drop 'related_task_id' column if it exists
    related_task_id_col_exists = conn.execute(
        sa.text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='notifications' AND column_name='related_task_id'
        """)
    ).fetchone()
    
    if related_task_id_col_exists:
        op.drop_column('notifications', 'related_task_id')
        print("Removed 'related_task_id' column from notifications table")
    
    # Check and drop 'data' column if it exists
    data_col_exists = conn.execute(
        sa.text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='notifications' AND column_name='data'
        """)
    ).fetchone()
    
    if data_col_exists:
        op.drop_column('notifications', 'data')
        print("Removed 'data' column from notifications table")
    
    # Check and drop 'read_at' column if it exists
    read_at_col_exists = conn.execute(
        sa.text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='notifications' AND column_name='read_at'
        """)
    ).fetchone()
    
    if read_at_col_exists:
        op.drop_column('notifications', 'read_at')
        print("Removed 'read_at' column from notifications table")