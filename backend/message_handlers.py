"""
Message Handlers Module
This module contains handlers for processing messages received from Kafka via Dapr
"""

from typing import Dict, Any
from backend.services.state_service import state_service
from backend.event_mapper import event_mapper
import json
import logging

# Set up logging
logger = logging.getLogger(__name__)

class MessageHandlers:
    """Class to handle different types of messages received from Kafka via Dapr"""
    
    @staticmethod
    async def handle_task_update_message(message_data: Dict[str, Any]) -> bool:
        """
        Handle task update messages received from the task-updates topic
        
        Args:
            message_data: The message payload received from Kafka
            
        Returns:
            bool: True if handled successfully, False otherwise
        """
        try:
            logger.info(f"Handling task update message: {json.dumps(message_data, indent=2)}")
            
            # Extract task information from the message
            task_id = message_data.get("task", {}).get("taskId")
            if not task_id:
                logger.error("No task ID found in task update message")
                return False
            
            # Update the task in the state store
            task_key = f"task:{task_id}"
            await state_service.save_state(task_key, message_data.get("task"))
            
            logger.info(f"Successfully updated task {task_id} in state store")
            return True
            
        except Exception as e:
            logger.error(f"Error handling task update message: {str(e)}")
            return False
    
    @staticmethod
    async def handle_reminder_message(message_data: Dict[str, Any]) -> bool:
        """
        Handle reminder messages received from the reminders topic
        
        Args:
            message_data: The message payload received from Kafka
            
        Returns:
            bool: True if handled successfully, False otherwise
        """
        try:
            logger.info(f"Handling reminder message: {json.dumps(message_data, indent=2)}")
            
            # Extract reminder information from the message
            reminder_data = message_data.get("reminder", {})
            if not reminder_data:
                logger.error("No reminder data found in reminder message")
                return False
            
            # Process the reminder - could involve sending notifications, etc.
            reminder_id = reminder_data.get("reminderId")
            if reminder_id:
                # Update the reminder state to mark it as notified
                reminder_key = f"reminder:{reminder_id}"
                
                # Update the notified flag
                reminder_data["notified"] = True
                await state_service.save_state(reminder_key, reminder_data)
                
                logger.info(f"Successfully processed reminder {reminder_id}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error handling reminder message: {str(e)}")
            return False
    
    @staticmethod
    async def handle_task_event_message(message_data: Dict[str, Any]) -> bool:
        """
        Handle task event messages received from the task-events topic
        
        Args:
            message_data: The message payload received from Kafka
            
        Returns:
            bool: True if handled successfully, False otherwise
        """
        try:
            logger.info(f"Handling task event message: {json.dumps(message_data, indent=2)}")
            
            event_type = message_data.get("eventType", "")
            
            if event_type == "task.created":
                # Handle task created event
                task_data = message_data.get("task", {})
                task_id = task_data.get("taskId")
                
                if task_id:
                    # Save the task in the state store
                    task_key = f"task:{task_id}"
                    await state_service.save_state(task_key, task_data)
                    
                    logger.info(f"Saved newly created task {task_id} in state store")
                    
            elif event_type == "task.deleted":
                # Handle task deleted event
                task_id = message_data.get("taskId")
                
                if task_id:
                    # Remove the task from the state store
                    task_key = f"task:{task_id}"
                    await state_service.delete_state(task_key)
                    
                    logger.info(f"Removed task {task_id} from state store")
            
            elif event_type == "task.updated":
                # Handle task updated event
                task_data = message_data.get("task", {})
                task_id = task_data.get("taskId")
                
                if task_id:
                    # Update the task in the state store
                    task_key = f"task:{task_id}"
                    await state_service.save_state(task_key, task_data)
                    
                    logger.info(f"Updated task {task_id} in state store")
            
            else:
                logger.warning(f"Unknown task event type: {event_type}")
                
            return True
            
        except Exception as e:
            logger.error(f"Error handling task event message: {str(e)}")
            return False
    
    @staticmethod
    async def route_message(topic: str, message_data: Dict[str, Any]) -> bool:
        """
        Route messages to appropriate handlers based on the topic
        
        Args:
            topic: The topic the message was received from
            message_data: The message payload
            
        Returns:
            bool: True if handled successfully, False otherwise
        """
        if topic == "task-updates":
            return await MessageHandlers.handle_task_update_message(message_data)
        elif topic == "reminders":
            return await MessageHandlers.handle_reminder_message(message_data)
        elif topic == "task-events":
            return await MessageHandlers.handle_task_event_message(message_data)
        else:
            logger.warning(f"No handler for topic: {topic}")
            return False

# Global instance
message_handlers = MessageHandlers()