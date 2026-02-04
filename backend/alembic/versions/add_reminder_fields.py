"""Add reminder fields to Task table

Revision ID: add_reminder_fields
Revises: add_remaining_recurrence_fields
Create Date: 2026-01-29 18:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'add_reminder_fields'
down_revision = 'add_remaining_recurrence_fields'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add reminder_time column if it doesn't exist
    try:
        op.execute("SELECT reminder_time FROM task LIMIT 1;")
    except:
        op.add_column('task', sa.Column('reminder_time', sa.DateTime(), nullable=True))

    # Add reminder_type column if it doesn't exist
    try:
        op.execute("SELECT reminder_type FROM task LIMIT 1;")
    except:
        op.add_column('task', sa.Column('reminder_type', sa.String(length=50), nullable=True))

    # Add reminder_offset column if it doesn't exist
    try:
        op.execute("SELECT reminder_offset FROM task LIMIT 1;")
    except:
        op.add_column('task', sa.Column('reminder_offset', sa.Integer(), nullable=True))


def downgrade() -> None:
    # Remove the reminder columns if they exist
    conn = op.get_bind()
    try:
        op.execute("SELECT reminder_time FROM task LIMIT 1;")
        op.drop_column('task', 'reminder_time')
    except:
        pass  # Column may not exist

    try:
        op.execute("SELECT reminder_type FROM task LIMIT 1;")
        op.drop_column('task', 'reminder_type')
    except:
        pass  # Column may not exist

    try:
        op.execute("SELECT reminder_offset FROM task LIMIT 1;")
        op.drop_column('task', 'reminder_offset')
    except:
        pass  # Column may not exist