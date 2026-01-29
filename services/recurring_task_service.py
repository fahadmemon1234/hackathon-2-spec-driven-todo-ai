import sys
import os

# Add the project root and backend directory to the Python path to resolve imports
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)  # Go up one level to project root
backend_dir = os.path.join(project_root, 'backend')

sys.path.insert(0, project_root)
sys.path.insert(0, backend_dir)

from kafka import KafkaConsumer
import json
import time
import logging
from datetime import datetime
from dateutil.rrule import rrule, DAILY, WEEKLY, MONTHLY
from dateutil.parser import parse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RecurringTaskService:
    def __init__(self):
        self.kafka_broker = os.getenv('KAFKA_BROKER', 'localhost:9092')
        self.consumer = KafkaConsumer(
            'task-events',
            bootstrap_servers=[self.kafka_broker],
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            group_id='recurring-task-group'
        )
        
    def parse_rrule(self, rrule_str, start_date):
        """Parse RRULE string and return next occurrence"""
        # Simple parsing for common RRULE patterns
        if 'FREQ=DAILY' in rrule_str:
            return start_date.replace(day=start_date.day + 1)
        elif 'FREQ=WEEKLY' in rrule_str:
            return start_date.replace(day=start_date.day + 7)
        elif 'FREQ=MONTHLY' in rrule_str:
            # Simple monthly calculation (add 30 days)
            return start_date.replace(day=min(start_date.day, 28))  # Handle month boundaries
        else:
            # Default to daily if unrecognized
            return start_date.replace(day=start_date.day + 1)
    
    def create_next_occurrence(self, task_data):
        """Create the next occurrence of a recurring task"""
        try:
            # In a real implementation, this would call the backend API to create a new task
            logger.info(f"Creating next occurrence for task {task_data.get('task_id')}")
            
            # Calculate next occurrence based on recurrence rule
            if task_data.get('recurrence_rule'):
                due_date = parse(task_data['due_date']) if task_data.get('due_date') else datetime.now()
                next_occurrence = self.parse_rrule(task_data['recurrence_rule'], due_date)
                
                # Prepare new task data
                new_task = {
                    'title': task_data['title'],
                    'description': task_data.get('description'),
                    'priority': task_data.get('priority', 'medium'),
                    'category': task_data.get('category'),
                    'tags': task_data.get('tags', []),
                    'due_date': next_occurrence.isoformat(),
                    'is_recurring': task_data.get('is_recurring', False),
                    'recurrence_rule': task_data.get('recurrence_rule'),
                    'user_id': task_data['user_id']
                }
                
                logger.info(f"Created next occurrence: {new_task}")
                
                # In a real implementation, this would call the backend API to create the new task
                # For now, we'll just log it
                print(f"New recurring task created: {new_task}")
                
        except Exception as e:
            logger.error(f"Error creating next occurrence: {e}")
    
    def start_consuming(self):
        """Start consuming task events from Kafka"""
        logger.info("Starting recurring task service...")
        try:
            for message in self.consumer:
                task_event = message.value
                event_type = task_event.get('event_type')
                
                # Only process completed events for recurring tasks
                if event_type == 'completed' and task_event.get('task_data', {}).get('is_recurring'):
                    logger.info(f"Processing completed recurring task: {task_event}")
                    self.create_next_occurrence(task_event['task_data'])
                
        except KeyboardInterrupt:
            logger.info("Shutting down recurring task service...")
        except Exception as e:
            logger.error(f"Error in recurring task service: {e}")

if __name__ == "__main__":
    service = RecurringTaskService()
    service.start_consuming()