#!/usr/bin/env python3
"""
Recurring Task Consumer Service

This service subscribes to the 'task-events' Kafka topic and processes
task completion events to generate the next instance of recurring tasks.
"""

import json
import logging
import sys
import os

# Add the project root and backend directory to the Python path to resolve imports
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)  # Go up one level to project root
backend_dir = os.path.join(project_root, 'backend')

sys.path.insert(0, project_root)
sys.path.insert(0, backend_dir)

from kafka import KafkaConsumer
from sqlmodel import create_engine, Session
from backend.models import Task, User  # Use absolute import from backend
from datetime import datetime
from backend.utils.recurrence_utils import calculate_next_occurrence, validate_recurrence_end_condition  # Use absolute import from backend
import signal
from typing import Optional


# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RecurringTaskConsumer:
    def __init__(self, kafka_bootstrap_servers: str = "localhost:9092", db_url: str = None):
        """
        Initialize the recurring task consumer.
        
        Args:
            kafka_bootstrap_servers: Kafka broker addresses
            db_url: Database connection URL
        """
        self.running = True
        self.kafka_bootstrap_servers = kafka_bootstrap_servers
        self.db_url = db_url or os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")
        
        # Create database engine
        self.engine = create_engine(self.db_url)
        
        # Initialize Kafka consumer
        self.consumer = KafkaConsumer(
            'task-events',
            bootstrap_servers=self.kafka_bootstrap_servers,
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='recurring-task-consumer-group'
        )
        
        # Handle shutdown signals
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """
        Handle shutdown signals gracefully.
        """
        logger.info(f"Received signal {signum}, shutting down...")
        self.running = False

    def process_task_completion_event(self, event_data: dict):
        """
        Process a task completion event and create the next recurring task instance if needed.
        
        Args:
            event_data: Dictionary containing task completion event data
        """
        try:
            event_type = event_data.get("event_type")
            
            if event_type != "task_completed":
                logger.debug(f"Ignoring non-completion event: {event_type}")
                return
            
            # Extract task information from the event
            task_id = event_data.get("task_id")
            recurrence_rule = event_data.get("recurrence_rule")
            
            if not recurrence_rule:
                logger.debug(f"Task {task_id} is not recurring, skipping")
                return
            
            # Connect to the database
            with Session(self.engine) as session:
                # Get the completed task
                completed_task = session.get(Task, task_id)
                
                if not completed_task:
                    logger.warning(f"Completed task {task_id} not found in database")
                    return
                
                # Check if recurrence should end based on end conditions
                should_end = validate_recurrence_end_condition(
                    completed_task.recurrence_rule,
                    completed_task.occurrence_number or 1,
                    completed_task.recurrence_max_count,
                    completed_task.recurrence_end_date
                )
                
                if should_end:
                    logger.info(f"Recurrence ending for task {task_id} based on end conditions")
                    return
                
                # Calculate the next occurrence date
                next_date = calculate_next_occurrence(
                    completed_task.recurrence_rule,
                    completed_task.due_date or datetime.utcnow()
                )
                
                if not next_date:
                    logger.warning(f"Could not calculate next occurrence for task {task_id}")
                    return
                
                # Check for idempotency: see if a similar task already exists
                existing_task = session.query(Task).filter(
                    Task.original_task_id == completed_task.id,
                    Task.due_date == next_date,
                    Task.user_id == completed_task.user_id
                ).first()
                
                if existing_task:
                    logger.info(f"Duplicate task detected for original_task_id {completed_task.id} and due_date {next_date}, skipping creation")
                    return
                
                # Create the next instance of the recurring task
                next_task = Task(
                    user_id=completed_task.user_id,
                    title=completed_task.title,
                    description=completed_task.description,
                    priority=completed_task.priority,
                    category=completed_task.category,
                    tags=completed_task.tags,
                    due_date=next_date,
                    is_recurring=completed_task.is_recurring,
                    recurrence_rule=completed_task.recurrence_rule,
                    recurrence_end_date=completed_task.recurrence_end_date,
                    recurrence_max_count=completed_task.recurrence_max_count,
                    original_task_id=completed_task.id,  # Reference to the original task
                    occurrence_number=(completed_task.occurrence_number or 1) + 1,  # Increment occurrence number
                    completed=False,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                
                # Calculate the next occurrence for the new task
                if completed_task.recurrence_rule:
                    next_occurrence = calculate_next_occurrence(completed_task.recurrence_rule, next_date)
                    next_task.next_occurrence = next_occurrence
                
                # Add the new task to the database
                session.add(next_task)
                session.commit()
                
                logger.info(f"Created next occurrence of recurring task {completed_task.id} as task {next_task.id} with due date {next_date}")
                
        except Exception as e:
            logger.error(f"Error processing task completion event: {str(e)}", exc_info=True)
            # In a production environment, you might want to send failed events to a dead-letter topic

    def run(self):
        """
        Run the consumer loop to process incoming events.
        """
        logger.info("Starting recurring task consumer...")
        
        try:
            for message in self.consumer:
                if not self.running:
                    break
                
                try:
                    event_data = message.value
                    logger.debug(f"Received event: {event_data}")
                    
                    self.process_task_completion_event(event_data)
                    
                except Exception as e:
                    logger.error(f"Error processing message: {str(e)}", exc_info=True)
                    
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt received, shutting down...")
        except Exception as e:
            logger.error(f"Unexpected error in consumer: {str(e)}", exc_info=True)
        finally:
            self.shutdown()

    def shutdown(self):
        """
        Shutdown the consumer gracefully.
        """
        logger.info("Shutting down consumer...")
        if self.consumer:
            self.consumer.close()
        logger.info("Consumer shut down successfully")


def main():
    """
    Main function to run the recurring task consumer.
    """
    # Get configuration from environment variables or use defaults
    kafka_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    db_url = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")
    
    # Create and run the consumer
    consumer = RecurringTaskConsumer(kafka_bootstrap_servers=kafka_servers, db_url=db_url)
    consumer.run()


if __name__ == "__main__":
    main()