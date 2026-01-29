"""
Kafka producer utility for publishing task events.
"""

from kafka import KafkaProducer
import json
import logging
from typing import Dict, Any
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TaskEventProducer:
    def __init__(self, bootstrap_servers: str = "localhost:9092"):
        """
        Initialize the Kafka producer for task events.
        
        Args:
            bootstrap_servers: Kafka broker addresses (comma-separated if multiple)
        """
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda k: k.encode('utf-8') if k else None,
            acks='all',  # Wait for all replicas to acknowledge
            retries=3,   # Retry sending messages up to 3 times
            linger_ms=5, #linger for 5ms to batch requests
        )
        self.topic = 'task-events'

    def publish_task_completion_event(self, task_data: Dict[str, Any]):
        """
        Publish a task completion event to the Kafka topic.
        
        Args:
            task_data: Dictionary containing task information
        """
        try:
            # Prepare the event message
            event_message = {
                "event_type": "task_completed",
                "timestamp": datetime.utcnow().isoformat(),
                "task_id": task_data.get("id"),
                "recurrence_rule": task_data.get("recurrence_rule"),
                "title": task_data.get("title"),
                "description": task_data.get("description"),
                "due_date": task_data.get("due_date").isoformat() if task_data.get("due_date") else None,
                "urgency": task_data.get("priority", "medium"),  # Using priority as urgency
                "tags": task_data.get("tags", []),
                "user_id": task_data.get("user_id"),
                "original_task_id": task_data.get("original_task_id"),
                "occurrence_number": task_data.get("occurrence_number", 1),
                "recurrence_end_date": task_data.get("recurrence_end_date").isoformat() if task_data.get("recurrence_end_date") else None,
                "recurrence_max_count": task_data.get("recurrence_max_count")
            }

            # Send the message to Kafka
            future = self.producer.send(self.topic, key=str(task_data.get("id")), value=event_message)
            
            # Block until the message is sent (with timeout)
            record_metadata = future.get(timeout=10)
            
            logger.info(f"Task completion event published to topic '{self.topic}' "
                       f"partition {record_metadata.partition} offset {record_metadata.offset}")
                       
        except Exception as e:
            logger.error(f"Failed to publish task completion event: {str(e)}")
            raise

    def close(self):
        """
        Close the Kafka producer connection.
        """
        self.producer.close()


# Global instance of the producer (will be initialized when needed)
task_event_producer = None


def get_task_event_producer(bootstrap_servers: str = "localhost:9092") -> TaskEventProducer:
    """
    Get or create a singleton instance of the task event producer.
    
    Args:
        bootstrap_servers: Kafka broker addresses
        
    Returns:
        TaskEventProducer instance
    """
    global task_event_producer
    if task_event_producer is None:
        task_event_producer = TaskEventProducer(bootstrap_servers)
    return task_event_producer