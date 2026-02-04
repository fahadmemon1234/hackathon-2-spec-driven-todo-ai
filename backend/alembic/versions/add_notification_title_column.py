"""Add missing columns to notifications table

Revision ID: add_notification_title_column
Revises: add_remaining_recurrence_fields
Create Date: 2026-01-30 15:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'add_notification_title_column'
down_revision = 'add_reminder_fields'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Check if columns exist and add them if they don't
    conn = op.get_bind()

    # Add title column if it doesn't exist
    try:
        op.execute("SELECT title FROM notifications LIMIT 1;")
    except:
        op.add_column('notifications', sa.Column('title', sa.String(length=200), nullable=True, server_default='Notification'))
        op.execute("UPDATE notifications SET title = 'Notification' WHERE title IS NULL")
        op.alter_column('notifications', 'title', nullable=False)

    # Add other columns if they don't exist
    try:
        op.execute("SELECT related_task_id FROM notifications LIMIT 1;")
    except:
        op.add_column('notifications', sa.Column('related_task_id', sa.String(), nullable=True))

    try:
        op.execute("SELECT data FROM notifications LIMIT 1;")
    except:
        op.add_column('notifications', sa.Column('data', postgresql.JSON, nullable=True))

    try:
        op.execute("SELECT read_at FROM notifications LIMIT 1;")
    except:
        op.add_column('notifications', sa.Column('read_at', sa.DateTime(), nullable=True))


def downgrade() -> None:
    # Remove the columns if they exist
    conn = op.get_bind()
    try:
        op.execute("SELECT title FROM notifications LIMIT 1;")
        op.drop_column('notifications', 'title')
    except:
        pass  # Column may not exist

    try:
        op.execute("SELECT related_task_id FROM notifications LIMIT 1;")
        op.drop_column('notifications', 'related_task_id')
    except:
        pass  # Column may not exist

    try:
        op.execute("SELECT data FROM notifications LIMIT 1;")
        op.drop_column('notifications', 'data')
    except:
        pass  # Column may not exist

    try:
        op.execute("SELECT read_at FROM notifications LIMIT 1;")
        op.drop_column('notifications', 'read_at')
    except:
        pass  # Column may not exist