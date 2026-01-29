"""
Cron Service for Processing Scheduled Tasks

This service handles periodic tasks like checking for due reminders.
"""

import asyncio
import logging
import time
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from services.reminder_scheduler import get_reminder_scheduler


class CronService:
    def __init__(self):
        """
        Initialize the cron service.
        """
        self.scheduler = BackgroundScheduler()
        self.reminder_scheduler = get_reminder_scheduler()
        self.logger = logging.getLogger(__name__)

    def start(self):
        """
        Start the cron service.
        """
        # Schedule the reminder checker to run every minute
        self.scheduler.add_job(
            func=self.check_and_process_due_reminders,
            trigger=IntervalTrigger(seconds=60),
            id='reminder_checker',
            name='Check for due reminders',
            replace_existing=True
        )

        # Start the scheduler
        self.scheduler.start()
        self.logger.info("Cron service started")

        # Keep the service alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        """
        Stop the cron service.
        """
        self.scheduler.shutdown()
        self.logger.info("Cron service stopped")

    def check_and_process_due_reminders(self):
        """
        Check for reminders that are due to be sent and process them.
        """
        try:
            self.logger.info("Checking for due reminders...")
            sent_count = self.reminder_scheduler.check_and_send_due_reminders()
            self.logger.info(f"Processed {sent_count} due reminders")
        except Exception as e:
            self.logger.error(f"Error processing due reminders: {str(e)}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    cron_service = CronService()
    try:
        cron_service.start()
    except KeyboardInterrupt:
        print("Shutting down cron service...")
        cron_service.stop()