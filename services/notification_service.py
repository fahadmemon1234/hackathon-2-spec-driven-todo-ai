from kafka import KafkaConsumer
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NotificationService:
    def __init__(self):
        self.kafka_broker = os.getenv('KAFKA_BROKER', 'localhost:9092')
        self.consumer = KafkaConsumer(
            'reminders',
            bootstrap_servers=[self.kafka_broker],
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            group_id='notification-group'
        )
        
    def send_notification(self, reminder_data):
        """Send notification to user"""
        try:
            # In a real implementation, this would send an actual notification
            # via email, push notification, etc.
            logger.info(f"Sending notification for task {reminder_data.get('task_id')}")
            logger.info(f"Title: {reminder_data.get('title')}")
            logger.info(f"Due at: {reminder_data.get('due_at')}")
            
            # Placeholder for actual notification logic
            # This could be email, SMS, push notification, etc.
            print(f"Notification sent: {reminder_data}")
            
        except Exception as e:
            logger.error(f"Error sending notification: {e}")
    
    def start_consuming(self):
        """Start consuming reminder events from Kafka"""
        logger.info("Starting notification service...")
        try:
            for message in self.consumer:
                reminder_data = message.value
                logger.info(f"Received reminder: {reminder_data}")
                
                # Process the reminder
                self.send_notification(reminder_data)
                
        except KeyboardInterrupt:
            logger.info("Shutting down notification service...")
        except Exception as e:
            logger.error(f"Error in notification service: {e}")

if __name__ == "__main__":
    service = NotificationService()
    service.start_consuming()