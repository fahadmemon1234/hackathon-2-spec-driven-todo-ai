"""
Event Publisher Utility

This module provides classes and functions for publishing
events to the event-driven architecture using Dapr.
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, Optional

import sys
import os
# Add the backend directory to the path so we can import from models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.models import Task


class EventPublisher:
    """Class to handle publishing events to the event-driven architecture."""

    def __init__(self):
        """Initialize the event publisher."""
        try:
            from dapr.clients import DaprClient
            self.dapr_client = DaprClient()
            self.dapr_available = True
        except ImportError:
            print("Dapr not available, events will be logged instead")
            self.dapr_available = False

        # Initialize Kafka producer for real-time notifications
        try:
            from kafka import KafkaProducer
            kafka_broker = os.getenv('KAFKA_BROKERS', 'localhost:9092')
            # Try to create the producer but don't connect immediately
            self.kafka_producer = KafkaProducer(
                bootstrap_servers=[kafka_broker],
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                api_version=(0, 10, 1),  # Specify API version to avoid auto-discovery
                linger_ms=50,  # Wait up to 50ms to batch messages
                retries=3  # Retry sending messages up to 3 times
            )
            self.kafka_available = True
        except ImportError:
            print("Kafka not available for real-time notifications")
            self.kafka_available = False
        except Exception as e:
            print(f"Kafka connection error: {e}. Real-time notifications will be disabled.")
            self.kafka_available = False

    def publish_task_event(self, event_type: str, task: Task, user_id: str):
        """
        Publish a task event to the task-events topic.

        Args:
            event_type: Type of event ('created', 'updated', 'completed', 'deleted')
            task: The task object
            user_id: The user ID associated with the task
        """
        event_data = {
            "event_type": event_type,
            "task_id": task.id,
            "user_id": user_id,
            "task_data": {
                "id": task.id,
                "user_id": task.user_id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "priority": task.priority,
                "tags": task.tags,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "is_recurring": task.is_recurring,
                "recurrence_rule": task.recurrence_rule,
                "next_occurrence": task.next_occurrence.isoformat() if task.next_occurrence else None
            },
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

        # Publish to Dapr pub/sub
        if self.dapr_available:
            try:
                with self.dapr_client as client:
                    client.publish_event(
                        pubsub_name='taskpubsub',  # This should match the Dapr pubsub component name
                        topic_name='task-events',
                        data=json.dumps(event_data),
                        data_content_type='application/json'
                    )
                print(f"Published {event_type} event for task {task.id} via Dapr")
            except Exception as e:
                print(f"Failed to publish {event_type} event for task {task.id} via Dapr: {e}")
                print("Event data:", json.dumps(event_data, indent=2))
        else:
            # Log the event instead of publishing it
            print(f"Dapr not available. Would publish {event_type} event for task {task.id}")
            print("Event data:", json.dumps(event_data, indent=2))

        # Also publish to notifications topic for real-time updates
        if self.kafka_available:
            try:
                # Create a simplified notification for real-time updates
                notification_data = {
                    "type": "task_update",
                    "event_type": event_type,
                    "task_id": task.id,
                    "user_id": user_id,
                    "title": task.title,
                    "completed": task.completed,
                    "priority": task.priority,
                    "due_date": task.due_date.isoformat() if task.due_date else None,
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }

                self.kafka_producer.send('notifications', notification_data)
                self.kafka_producer.flush()  # Ensure the message is sent
                print(f"Published real-time notification for task {task.id}")
            except Exception as e:
                print(f"Failed to publish real-time notification for task {task.id}: {e}")
        else:
            print(f"Kafka not available for real-time notifications for task {task.id}")

    def publish_reminder_event(self, task: Task, user_id: str):
        """
        Publish a reminder event to the reminders topic.

        Args:
            task: The task object with due date
            user_id: The user ID associated with the task
        """
        if not task.due_date:
            print("Task has no due date, skipping reminder event")
            return

        # Calculate reminder time (1 hour before due date)
        # For now, we'll use a simple calculation - in a real system you'd want to be more sophisticated
        from datetime import timedelta
        remind_at = task.due_date - timedelta(hours=1)

        event_data = {
            "task_id": task.id,
            "user_id": user_id,
            "title": task.title,
            "due_at": task.due_date.isoformat(),
            "remind_at": remind_at.isoformat(),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

        # Publish to Dapr pub/sub
        if self.dapr_available:
            try:
                with self.dapr_client as client:
                    client.publish_event(
                        pubsub_name='reminderpubsub',  # This should match the Dapr pubsub component name
                        topic_name='reminders',
                        data=json.dumps(event_data),
                        data_content_type='application/json'
                    )
                print(f"Published reminder event for task {task.id}, due at {task.due_date} via Dapr")
            except Exception as e:
                print(f"Failed to publish reminder event for task {task.id} via Dapr: {e}")
                print("Event data:", json.dumps(event_data, indent=2))
        else:
            # Log the event instead of publishing it
            print(f"Dapr not available. Would publish reminder event for task {task.id}")
            print("Event data:", json.dumps(event_data, indent=2))

        # Also publish to notifications topic for real-time updates
        if self.kafka_available:
            try:
                # Create a simplified notification for real-time updates
                notification_data = {
                    "type": "reminder",
                    "task_id": task.id,
                    "user_id": user_id,
                    "title": task.title,
                    "due_at": task.due_date.isoformat(),
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }

                self.kafka_producer.send('notifications', notification_data)
                self.kafka_producer.flush()  # Ensure the message is sent
                print(f"Published real-time reminder notification for task {task.id}")
            except Exception as e:
                print(f"Failed to publish real-time reminder notification for task {task.id}: {e}")
        else:
            print(f"Kafka not available for real-time reminder notifications for task {task.id}")

    def close(self):
        """Close the Dapr client and Kafka producer connections."""
        if self.dapr_available and hasattr(self, 'dapr_client'):
            self.dapr_client.close()

        if self.kafka_available and hasattr(self, 'kafka_producer'):
            self.kafka_producer.close()