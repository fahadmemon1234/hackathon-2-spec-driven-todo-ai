"""
Reminder Scheduler Service

This service handles scheduling and sending reminders for tasks with due dates.
It integrates with Kafka to publish reminder events.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from sqlmodel import create_engine, Session, select
import sys
import os
# Add the backend directory to the path so we can import from models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import Task
from utils.event_publisher import EventPublisher


class ReminderScheduler:
    def __init__(self, db_url: str = None):
        """
        Initialize the reminder scheduler.

        Args:
            db_url: Database connection URL
        """
        self.db_url = db_url or os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")
        self.engine = create_engine(self.db_url)
        self.logger = logging.getLogger(__name__)
        self.event_publisher = EventPublisher()

    def calculate_reminder_time(self, due_date: datetime, offset_minutes: Optional[int] = None) -> datetime:
        """
        Calculate the reminder time based on the due date and offset.

        Args:
            due_date: The due date of the task
            offset_minutes: Minutes before due date to send reminder (default: 60 minutes)

        Returns:
            The calculated reminder time
        """
        if offset_minutes is None:
            # Default to 1 hour before due date
            offset_minutes = 60
        
        return due_date - timedelta(minutes=offset_minutes)

    def schedule_reminder_for_task(self, task: Task) -> bool:
        """
        Schedule a reminder for a specific task.

        Args:
            task: The task to schedule a reminder for

        Returns:
            True if reminder was scheduled successfully, False otherwise
        """
        try:
            # Determine the reminder time based on task settings
            reminder_time = None
            
            if task.reminder_offset is not None:
                # Use the task-specific reminder offset
                reminder_time = self.calculate_reminder_time(task.due_date, task.reminder_offset)
            elif task.reminder_time is not None:
                # Use the specific reminder time set for the task
                reminder_time = task.reminder_time
            else:
                # Use default reminder time (1 hour before due date)
                reminder_time = self.calculate_reminder_time(task.due_date)
            
            # Check if the reminder time is in the past
            if reminder_time <= datetime.utcnow():
                self.logger.warning(f"Reminder time for task {task.id} is in the past: {reminder_time}")
                return False
            
            # Publish the reminder event to Kafka
            reminder_data = {
                "task_id": task.id,
                "user_id": task.user_id,
                "title": task.title,
                "due_at": task.due_date.isoformat() if task.due_date else None,
                "remind_at": reminder_time.isoformat(),
                "reminder_type": task.reminder_type,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            
            # Publish the reminder event
            self.event_publisher.publish_reminder_event(task, task.user_id)
            
            self.logger.info(f"Scheduled reminder for task {task.id} at {reminder_time}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error scheduling reminder for task {task.id}: {str(e)}")
            return False

    def schedule_reminders_for_user(self, user_id: str) -> int:
        """
        Schedule reminders for all tasks with due dates for a specific user.

        Args:
            user_id: The user ID to schedule reminders for

        Returns:
            The number of reminders scheduled
        """
        scheduled_count = 0
        
        with Session(self.engine) as session:
            # Get all tasks with due dates for the user that are not completed
            statement = select(Task).where(
                Task.user_id == user_id,
                Task.due_date.is_not(None),
                Task.completed == False
            )
            
            tasks = session.exec(statement).all()
            
            for task in tasks:
                if self.schedule_reminder_for_task(task):
                    scheduled_count += 1
        
        self.logger.info(f"Scheduled {scheduled_count} reminders for user {user_id}")
        return scheduled_count

    def schedule_reminders_for_all_users(self) -> int:
        """
        Schedule reminders for all tasks with due dates for all users.

        Returns:
            The total number of reminders scheduled
        """
        total_scheduled = 0
        
        with Session(self.engine) as session:
            # Get all tasks with due dates that are not completed
            statement = select(Task).where(
                Task.due_date.is_not(None),
                Task.completed == False
            )
            
            tasks = session.exec(statement).all()
            
            for task in tasks:
                if self.schedule_reminder_for_task(task):
                    total_scheduled += 1
        
        self.logger.info(f"Scheduled {total_scheduled} reminders for all users")
        return total_scheduled

    def check_and_send_due_reminders(self) -> int:
        """
        Check for reminders that are due to be sent and send them.

        Returns:
            The number of reminders sent
        """
        sent_count = 0

        # In a real implementation, this would:
        # 1. Query the state store or database for reminders where remind_at <= now and not sent
        # 2. For each due reminder:
        #    - Mark as sent in state store
        #    - Publish reminder event via pub/sub
        #    - Send actual notification (email, push, etc.)

        # For this implementation, we'll use the database to find tasks with due dates
        # that are approaching and send reminders for them
        with Session(self.engine) as session:
            # Find tasks with due dates that are within the next 10 minutes (for demo purposes)
            # In a real system, you would check for reminders that are due NOW
            from datetime import timedelta
            from datetime import timezone
            now = datetime.now(timezone.utc).replace(tzinfo=None)  # Make sure it's timezone-naive
            upcoming_threshold = now + timedelta(minutes=10)  # Check for reminders due in next 10 mins

            # Get tasks that have due dates within the threshold and are not completed
            statement = select(Task).where(
                Task.due_date <= upcoming_threshold,
                Task.due_date >= now,
                Task.completed == False
            )

            upcoming_tasks = session.exec(statement).all()

            for task in upcoming_tasks:
                # Check if a reminder should be sent based on the reminder offset
                if task.reminder_offset is not None:
                    reminder_time = task.due_date - timedelta(minutes=task.reminder_offset)
                    # Ensure both datetimes are timezone-naive for comparison
                    if task.due_date.tzinfo is not None:
                        task_due_date_naive = task.due_date.replace(tzinfo=None)
                    else:
                        task_due_date_naive = task.due_date

                    if reminder_time.tzinfo is not None:
                        reminder_time_naive = reminder_time.replace(tzinfo=None)
                    else:
                        reminder_time_naive = reminder_time

                    if now >= reminder_time_naive:
                        # Send the reminder
                        self.event_publisher.publish_reminder_event(task, task.user_id)
                        sent_count += 1
                        self.logger.info(f"Sent reminder for task {task.id} due at {task.due_date}")
                elif task.reminder_time is not None:
                    # If a specific reminder time is set, check if it's time to send
                    # Ensure both datetimes are timezone-naive for comparison
                    reminder_time = task.reminder_time
                    if reminder_time.tzinfo is not None:
                        reminder_time_naive = reminder_time.replace(tzinfo=None)
                    else:
                        reminder_time_naive = reminder_time

                    if now >= reminder_time_naive:
                        # Send the reminder
                        self.event_publisher.publish_reminder_event(task, task.user_id)
                        sent_count += 1
                        self.logger.info(f"Sent reminder for task {task.id} due at {task.due_date}")
                else:
                    # Default: send reminder 1 hour before due date
                    default_reminder_time = task.due_date - timedelta(hours=1)
                    # Ensure both datetimes are timezone-naive for comparison
                    if task.due_date.tzinfo is not None:
                        task_due_date_naive = task.due_date.replace(tzinfo=None)
                    else:
                        task_due_date_naive = task.due_date

                    if default_reminder_time.tzinfo is not None:
                        default_reminder_time_naive = default_reminder_time.replace(tzinfo=None)
                    else:
                        default_reminder_time_naive = default_reminder_time

                    if now >= default_reminder_time_naive:
                        # Send the reminder
                        self.event_publisher.publish_reminder_event(task, task.user_id)
                        sent_count += 1
                        self.logger.info(f"Sent reminder for task {task.id} due at {task.due_date}")

        self.logger.info(f"Checked for due reminders, sent {sent_count}")
        return sent_count

    def close(self):
        """
        Close resources used by the reminder scheduler.
        """
        self.event_publisher.close()


# Global instance for convenience
reminder_scheduler = None


def get_reminder_scheduler(db_url: str = None) -> ReminderScheduler:
    """
    Get or create a singleton instance of the reminder scheduler.

    Args:
        db_url: Database connection URL

    Returns:
        A ReminderScheduler instance
    """
    global reminder_scheduler
    if reminder_scheduler is None:
        reminder_scheduler = ReminderScheduler(db_url)
    return reminder_scheduler


if __name__ == "__main__":
    # Example usage
    import time
    
    logging.basicConfig(level=logging.INFO)
    
    scheduler = get_reminder_scheduler()
    
    try:
        # Schedule reminders for all users
        count = scheduler.schedule_reminders_for_all_users()
        print(f"Scheduled {count} reminders")
        
        # Continuously check for due reminders
        while True:
            scheduler.check_and_send_due_reminders()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        print("Shutting down reminder scheduler...")
    finally:
        scheduler.close()