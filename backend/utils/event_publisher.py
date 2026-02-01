"""
Event Publisher Utility

This module provides classes and functions for publishing
events to the event-driven architecture using Dapr.
"""

import json
import logging
from datetime import datetime, timezone
from typing import Dict, Any, Optional

import sys
import os
# Add the backend directory to the path so we can import from models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import configuration
from ..config import KAFKA_BROKERS

from models import Task


class EventPublisher:
    """Class to handle publishing events to the event-driven architecture."""

    def __init__(self):
        """Initialize the event publisher."""
        self.dapr_available = False
        self.kafka_available = False

        # Initialize Dapr client with proper error handling
        try:
            from dapr.clients import DaprClient
            # Initialize Dapr client - in Docker environment, it should automatically connect to the sidecar
            # Check if DAPR_HTTP_PORT is available before initializing
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('localhost', int(os.getenv('DAPR_HTTP_PORT', 3500))))
            sock.close()

            if result == 0:  # Port is available
                self.dapr_client = DaprClient()
                self.dapr_available = True
                print("Dapr client initialized successfully")
            else:
                print("Dapr sidecar not available, events will be logged instead")
                self.dapr_client = None
        except ImportError:
            print("Dapr not available, events will be logged instead")
            self.dapr_client = None
        except ConnectionRefusedError as e:
            print(f"Dapr connection refused: {e}. Dapr may not be running. Events will be handled via fallback mechanisms.")
            self.dapr_client = None
        except Exception as e:
            print(f"Dapr connection error: {e}. Events will be handled via fallback mechanisms.")
            self.dapr_client = None

        # Initialize Kafka producer for real-time notifications
        try:
            from kafka import KafkaProducer

            # Create the producer with proper error handling
            self.kafka_producer = KafkaProducer(
                bootstrap_servers=[KAFKA_BROKERS],
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                api_version=(0, 10, 1),  # Specify API version to avoid auto-discovery
                linger_ms=50,  # Wait up to 50ms to batch messages
                retries=0,  # No retries to prevent blocking
                request_timeout_ms=3000,  # 3 seconds timeout for requests
                max_block_ms=1000,  # 1 second to wait for buffer space
                # Disable metadata fetching on startup to avoid DNS issues
                metadata_max_age_ms=300000,  # Refresh metadata every 5 minutes
            )
            self.kafka_available = True
            print("Kafka producer initialized successfully")
        except ImportError:
            print("Kafka not available for real-time notifications")
            self.kafka_producer = None
        except Exception as e:
            print(f"Kafka connection error: {e}. Real-time notifications will be disabled.")
            self.kafka_producer = None

    def publish_task_event(self, event_type: str, task: Task, user_id: str):
        """
        Publish a task event to the task-events topic.

        Args:
            event_type: Type of event ('created', 'updated', 'completed', 'deleted')
            task: The task object
            user_id: The user ID associated with the task
        """
        try:
            # Prepare event data with proper datetime handling
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
                "timestamp": datetime.now(timezone.utc).isoformat() + "Z"
            }

            # Publish to Dapr pub/sub
            if self.dapr_client:
                try:
                    # Use the Dapr client directly (not as context manager to avoid repeated connections)
                    self.dapr_client.publish_event(
                        pubsub_name=os.getenv('DAPR_PUBSUB_NAME', 'kafka-pubsub'),  # Use configured pubsub name
                        topic_name='task-events',
                        data=json.dumps(event_data),
                        data_content_type='application/json'
                    )
                    print(f"Published {event_data['event_type']} event for task {task.id} via Dapr")
                except Exception as e:
                    print(f"Failed to publish {event_data['event_type']} event for task {task.id} via Dapr: {e}")
                    print("Event data:", json.dumps(event_data, indent=2))
                    # Don't raise exception - allow the operation to continue even if Dapr fails
            else:
                # Log the event instead of publishing it
                print(f"Dapr not available. Would publish {event_data['event_type']} event for task {task.id}")
                print("Event data:", json.dumps(event_data, indent=2))

            # Also publish to notifications topic for real-time updates
            if self.kafka_producer:
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
                        "timestamp": datetime.now(timezone.utc).isoformat() + "Z"
                    }

                    self.kafka_producer.send('notifications', notification_data)
                    # Don't flush to avoid blocking the main operation
                    print(f"Published real-time notification for task {task.id}")
                except Exception as e:
                    print(f"Failed to publish real-time notification for task {task.id}: {e}")
                    # Don't raise exception - allow the operation to continue even if Kafka fails
            else:
                print(f"Kafka not available for real-time notifications for task {task.id}")

        except Exception as e:
            print(f"Error in publish_task_event: {e}")
            import traceback
            traceback.print_exc()
            # Don't raise exception - allow the operation to continue even if there's an error

    def publish_reminder_event(self, task: Task, user_id: str):
        """
        Publish a reminder event to the reminders topic.

        Args:
            task: The task object with due date
            user_id: The user ID associated with the task
        """
        try:
            if not task.due_date:
                print("Task has no due date, skipping reminder event")
                return

            # Calculate reminder time based on task settings
            from datetime import timedelta
            if task.reminder_offset is not None:
                # Use the task-specific reminder offset
                remind_at = task.due_date - timedelta(minutes=task.reminder_offset)
            else:
                # Use default reminder time (1 hour before due date)
                remind_at = task.due_date - timedelta(hours=1)

            event_data = {
                "task_id": task.id,
                "user_id": user_id,
                "title": task.title,
                "due_at": task.due_date.isoformat() if task.due_date else None,
                "remind_at": remind_at.isoformat() if remind_at else None,
                "reminder_type": task.reminder_type,
                "reminder_offset": task.reminder_offset,
                "timestamp": datetime.now(timezone.utc).isoformat() + "Z"
            }

            # Publish to Dapr pub/sub
            if self.dapr_client:
                try:
                    self.dapr_client.publish_event(
                        pubsub_name=os.getenv('DAPR_PUBSUB_NAME', 'kafka-pubsub'),  # Use configured pubsub name
                        topic_name='reminders',
                        data=json.dumps(event_data),
                        data_content_type='application/json'
                    )
                    print(f"Published reminder event for task {task.id}, due at {event_data['due_at']} via Dapr")
                except Exception as e:
                    print(f"Failed to publish reminder event for task {task.id} via Dapr: {e}")
                    print("Event data:", json.dumps(event_data, indent=2))
                    # Don't raise exception - allow the operation to continue even if Dapr fails
            else:
                # Log the event instead of publishing it
                print(f"Dapr not available. Would publish reminder event for task {task.id}")
                print("Event data:", json.dumps(event_data, indent=2))

            # Also publish to Kafka for the notification service
            if self.kafka_producer:
                try:
                    # Create a simplified notification for the notification service
                    notification_data = {
                        "type": "reminder",
                        "task_id": task.id,
                        "user_id": user_id,
                        "title": task.title,
                        "due_at": task.due_date.isoformat() if task.due_date else None,
                        "remind_at": remind_at.isoformat() if remind_at else None,
                        "reminder_type": task.reminder_type,
                        "timestamp": datetime.now(timezone.utc).isoformat() + "Z"
                    }

                    self.kafka_producer.send('reminders', notification_data)
                    # Don't flush to avoid blocking the main operation
                    print(f"Published reminder event to Kafka for task {task.id}")
                except Exception as e:
                    print(f"Failed to publish reminder event to Kafka for task {task.id}: {e}")
                    # Don't raise exception - allow the operation to continue even if Kafka fails
            else:
                print(f"Kafka not available for reminder events for task {task.id}")

        except Exception as e:
            print(f"Error in publish_reminder_event: {e}")
            import traceback
            traceback.print_exc()
            # Don't raise exception - allow the operation to continue even if there's an error

    def publish_reminder_scheduled_event(self, task: Task, user_id: str, reminder_time: datetime):
        """
        Publish an event indicating that a reminder has been scheduled.

        Args:
            task: The task object with due date
            user_id: The user ID associated with the task
            reminder_time: The time when the reminder is scheduled
        """
        try:
            event_data = {
                "task_id": task.id,
                "user_id": user_id,
                "title": task.title,
                "due_at": task.due_date.isoformat() if task.due_date else None,
                "scheduled_reminder_at": reminder_time.isoformat() if reminder_time else None,
                "reminder_type": task.reminder_type,
                "timestamp": datetime.now(timezone.utc).isoformat() + "Z"
            }

            # Publish to Dapr pub/sub
            if self.dapr_client:
                try:
                    self.dapr_client.publish_event(
                        pubsub_name=os.getenv('DAPR_PUBSUB_NAME', 'kafka-pubsub'),  # Use configured pubsub name
                        topic_name='reminders',
                        data=json.dumps(event_data),
                        data_content_type='application/json'
                    )
                    print(f"Published reminder scheduled event for task {task.id} at {event_data['scheduled_reminder_at']} via Dapr")
                except Exception as e:
                    print(f"Failed to publish reminder scheduled event for task {task.id} via Dapr: {e}")
                    print("Event data:", json.dumps(event_data, indent=2))
                    # Don't raise exception - allow the operation to continue even if Dapr fails

            # Also publish to Kafka for the notification service
            if self.kafka_producer:
                try:
                    self.kafka_producer.send('reminders', event_data)
                    # Don't flush to avoid blocking the main operation
                    print(f"Published reminder scheduled event to Kafka for task {task.id}")
                except Exception as e:
                    print(f"Failed to publish reminder scheduled event to Kafka for task {task.id}: {e}")
                    # Don't raise exception - allow the operation to continue even if Kafka fails

        except Exception as e:
            print(f"Error in publish_reminder_scheduled_event: {e}")
            import traceback
            traceback.print_exc()
            # Don't raise exception - allow the operation to continue even if there's an error

    def close(self):
        """Close the Dapr client and Kafka producer connections."""
        try:
            if self.dapr_client:
                self.dapr_client.close()
        except Exception as e:
            print(f"Error closing Dapr client: {e}")

        try:
            if self.kafka_producer:
                self.kafka_producer.close()
        except Exception as e:
            print(f"Error closing Kafka producer: {e}")