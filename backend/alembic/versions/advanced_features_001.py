"""Add new fields to Task table for advanced features

Revision ID: advanced_features_001
Revises:
Create Date: 2026-01-19 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'advanced_features_001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add new columns to the task table
    op.add_column('task', sa.Column('tags', postgresql.JSON, nullable=True, server_default='[]'))
    op.add_column('task', sa.Column('due_date', sa.DateTime(), nullable=True))
    op.add_column('task', sa.Column('is_recurring', sa.Boolean(), nullable=True, server_default='false'))
    op.add_column('task', sa.Column('recurrence_rule', sa.String(length=200), nullable=True))
    op.add_column('task', sa.Column('next_occurrence', sa.DateTime(), nullable=True))
    
    # Update the default value for is_recurring to false
    op.execute("UPDATE task SET is_recurring = false WHERE is_recurring IS NULL")
    op.alter_column('task', 'is_recurring', nullable=False, server_default='false')
    
    # Update the default value for tags to empty array
    op.execute("UPDATE task SET tags = '[]' WHERE tags IS NULL")
    op.alter_column('task', 'tags', nullable=False, server_default='[]')
    
    # Update priority column to include 'urgent' value
    # First, drop the existing constraint
    op.drop_constraint('task_priority_check', 'task', type_='check')
    # Then recreate it with the new values
    op.create_check_constraint('task_priority_check', 'task', "priority IN ('low', 'medium', 'high', 'urgent')")
    
    # Create indexes for improved query performance
    op.create_index('ix_task_user_id_priority', 'task', ['user_id', 'priority'])
    op.create_index('ix_task_user_id_due_date', 'task', ['user_id', 'due_date'])
    op.create_index('ix_task_user_id_is_recurring', 'task', ['user_id', 'is_recurring'])
    op.create_index('ix_task_tags', 'task', ['tags'], postgresql_using='gin')


def downgrade() -> None:
    # Drop indexes
    op.drop_index('ix_task_tags', table_name='task')
    op.drop_index('ix_task_user_id_is_recurring', table_name='task')
    op.drop_index('ix_task_user_id_due_date', table_name='task')
    op.drop_index('ix_task_user_id_priority', table_name='task')
    
    # Remove new columns
    op.drop_column('task', 'next_occurrence')
    op.drop_column('task', 'recurrence_rule')
    op.drop_column('task', 'is_recurring')
    op.drop_column('task', 'due_date')
    op.drop_column('task', 'tags')
    
    # Restore the original priority constraint
    op.drop_constraint('task_priority_check', 'task', type_='check')
    op.create_check_constraint('task_priority_check', 'task', "priority IN ('low', 'medium', 'high')")