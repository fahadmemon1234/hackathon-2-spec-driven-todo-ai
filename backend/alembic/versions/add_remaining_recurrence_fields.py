"""Add missing recurrence fields if they don't exist

Revision ID: add_remaining_recurrence_fields
Revises: advanced_features_001
Create Date: 2026-01-27 17:27:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'add_remaining_recurrence_fields'
down_revision = 'advanced_features_001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Check if columns exist and add them if they don't
    conn = op.get_bind()
    
    # Add recurrence_end_date column if it doesn't exist
    try:
        op.execute("SELECT recurrence_end_date FROM task LIMIT 1;")
    except:
        op.add_column('task', sa.Column('recurrence_end_date', sa.DateTime(), nullable=True))

    # Add recurrence_max_count column if it doesn't exist
    try:
        op.execute("SELECT recurrence_max_count FROM task LIMIT 1;")
    except:
        op.add_column('task', sa.Column('recurrence_max_count', sa.Integer(), nullable=True))

    # Add original_task_id column if it doesn't exist
    try:
        op.execute("SELECT original_task_id FROM task LIMIT 1;")
    except:
        op.add_column('task', sa.Column('original_task_id', sa.Integer(), nullable=True))

    # Add occurrence_number column if it doesn't exist
    try:
        op.execute("SELECT occurrence_number FROM task LIMIT 1;")
    except:
        op.add_column('task', sa.Column('occurrence_number', sa.Integer(), nullable=True, server_default='1'))

    # Update the default value for occurrence_number to 1 if the column was added
    op.execute("UPDATE task SET occurrence_number = 1 WHERE occurrence_number IS NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'task' AND column_name = 'occurrence_number')")
    op.execute("UPDATE task SET occurrence_number = 1 WHERE occurrence_number = 0")  # In case it was added with 0 value

    # Add foreign key constraint for original_task_id if it doesn't exist
    try:
        # Check if the constraint already exists
        op.execute("SELECT constraint_name FROM information_schema.table_constraints WHERE constraint_name = 'fk_task_original_task_id';")
    except:
        op.create_foreign_key('fk_task_original_task_id', 'task', 'task', ['original_task_id'], ['id'])


def downgrade() -> None:
    # Drop foreign key constraint first
    try:
        op.drop_constraint('fk_task_original_task_id', 'task', type_='foreignkey')
    except:
        pass  # Constraint may not exist
    
    # Remove the columns if they exist
    conn = op.get_bind()
    try:
        op.execute("SELECT recurrence_end_date FROM task LIMIT 1;")
        op.drop_column('task', 'recurrence_end_date')
    except:
        pass  # Column may not exist

    try:
        op.execute("SELECT recurrence_max_count FROM task LIMIT 1;")
        op.drop_column('task', 'recurrence_max_count')
    except:
        pass  # Column may not exist

    try:
        op.execute("SELECT original_task_id FROM task LIMIT 1;")
        op.drop_column('task', 'original_task_id')
    except:
        pass  # Column may not exist

    try:
        op.execute("SELECT occurrence_number FROM task LIMIT 1;")
        op.drop_column('task', 'occurrence_number')
    except:
        pass  # Column may not exist