import sys
import os

# Add the project root and backend directory to the Python path to resolve imports
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)  # Go up one level to project root
backend_dir = os.path.join(project_root, 'backend')

sys.path.insert(0, project_root)
sys.path.insert(0, backend_dir)

from kafka import KafkaConsumer, KafkaProducer
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import logging
import asyncio
import websockets
import threading
from datetime import datetime
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NotificationService:
    def __init__(self):
        self.kafka_broker = os.getenv('KAFKA_BROKER', 'localhost:9092')
        self.websocket_uri = os.getenv('WEBSOCKET_URI', 'ws://websocket-service:8080/ws')
        self.consumer = KafkaConsumer(
            'reminders',
            bootstrap_servers=[self.kafka_broker],
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            group_id='notification-group'
        )

        # Producer for sending notifications to WebSocket service
        self.producer = KafkaProducer(
            bootstrap_servers=[self.kafka_broker],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

        # Store active WebSocket connections
        self.websocket_connections = set()

        # Email configuration
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        self.email_address = os.getenv('EMAIL_ADDRESS')
        self.email_password = os.getenv('EMAIL_PASSWORD')

    def send_real_time_notification(self, reminder_data: Dict[str, Any]):
        """Send real-time notification via WebSocket"""
        try:
            # Create notification payload
            notification_payload = {
                "type": "reminder",
                "task_id": reminder_data.get('task_id'),
                "user_id": reminder_data.get('user_id'),
                "title": reminder_data.get('title'),
                "due_at": reminder_data.get('due_at'),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }

            # Publish to notifications topic for WebSocket service to handle
            self.producer.send('notifications', notification_payload)
            self.producer.flush()  # Ensure the message is sent

            logger.info(f"Real-time notification published to WebSocket service: {notification_payload}")

        except Exception as e:
            logger.error(f"Error sending real-time notification: {e}")

    def send_email_notification(self, reminder_data: Dict[str, Any], user_email: str = None):
        """Send email notification to user"""
        try:
            if not self.email_address or not self.email_password:
                logger.warning("Email credentials not configured, skipping email notification")
                return

            # In a real implementation, we would fetch the user's email from a database
            # For now, we'll use a placeholder email
            recipient_email = user_email or f"{reminder_data.get('user_id')}@example.com"

            msg = MIMEMultipart()
            msg['From'] = self.email_address
            msg['To'] = recipient_email
            msg['Subject'] = f"Reminder: {reminder_data.get('title')}"

            body = f"""
            Hi there,

            This is a reminder for your task: {reminder_data.get('title')}

            Due Date: {reminder_data.get('due_at')}
            Task ID: {reminder_data.get('task_id')}

            Please complete this task on time.

            Best regards,
            Todo App Team
            """

            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_address, self.email_password)
            text = msg.as_string()
            server.sendmail(self.email_address, recipient_email, text)
            server.quit()

            logger.info(f"Email notification sent to {recipient_email}")

        except Exception as e:
            logger.error(f"Error sending email notification: {e}")

    def send_push_notification(self, reminder_data: Dict[str, Any]):
        """Send push notification to user (placeholder implementation)"""
        try:
            # In a real implementation, this would send a push notification via Firebase, APNs, etc.
            logger.info(f"Push notification sent for task {reminder_data.get('task_id')}")

            # Placeholder for push notification logic
            print(f"Push notification sent for task {reminder_data.get('task_id')}")

        except Exception as e:
            logger.error(f"Error sending push notification: {e}")

    def send_notification(self, reminder_data: Dict[str, Any]):
        """Send notification to user via multiple channels"""
        try:
            logger.info(f"Sending notification for task {reminder_data.get('task_id')}")
            logger.info(f"Title: {reminder_data.get('title')}")
            logger.info(f"Due at: {reminder_data.get('due_at')}")

            # Send real-time notification via WebSocket
            self.send_real_time_notification(reminder_data)

            # Send email notification
            self.send_email_notification(reminder_data)

            # Send push notification
            self.send_push_notification(reminder_data)

            logger.info(f"All notifications sent for task {reminder_data.get('task_id')}")

        except Exception as e:
            logger.error(f"Error sending notification: {e}")

    def start_websocket_handler(self):
        """Handle WebSocket connections for real-time notifications"""
        # This would normally be a separate async function
        # For now, we'll just log that this service can handle WebSocket connections
        logger.info("WebSocket handler initialized for real-time notifications")

    def start_consuming(self):
        """Start consuming reminder events from Kafka"""
        logger.info("Starting notification service with real-time capabilities...")

        # Initialize WebSocket handler
        self.start_websocket_handler()

        try:
            logger.info("Listening for reminder events...")
            for message in self.consumer:
                reminder_data = message.value
                logger.info(f"Received reminder: {reminder_data}")

                # Process the reminder with multiple notification channels
                self.send_notification(reminder_data)

        except KeyboardInterrupt:
            logger.info("Shutting down notification service...")
        except Exception as e:
            logger.error(f"Error in notification service: {e}")

if __name__ == "__main__":
    service = NotificationService()
    service.start_consuming()