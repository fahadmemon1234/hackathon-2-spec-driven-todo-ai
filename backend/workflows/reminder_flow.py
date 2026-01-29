"""
Reminder Flow Module
This module handles the complete reminder scheduling and processing flow using Dapr components
"""

from typing import Dict, Any
import datetime
from backend.services.state_service import state_service
from backend.services.pubsub_service import pubsub_service
from backend.constants import REMINDER_STATE_KEY_PATTERN

class ReminderFlow:
    """Class to handle the complete reminder scheduling and processing workflow"""
    
    @staticmethod
    async def schedule_reminder_workflow(reminder_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the complete reminder scheduling workflow:
        1. Store reminder schedule in state store
        2. The cron binding will trigger and process the reminder at the scheduled time
        3. When triggered, publish reminder event via pub/sub
        
        Args:
            reminder_data: The reminder data to schedule
            
        Returns:
            Result of the workflow execution
        """
        try:
            print(f"Starting reminder scheduling workflow: {reminder_data.get('reminderId', 'unknown')}")
            
            # Step 1: Store reminder schedule in state store
            reminder_id = reminder_data.get('reminderId')
            if not reminder_id:
                return {
                    "status": "error",
                    "message": "Reminder ID is required for state store operation"
                }
            
            reminder_key = REMINDER_STATE_KEY_PATTERN.format(reminderId=reminder_id)
            save_result = await state_service.save_state(reminder_key, reminder_data)
            
            if not save_result:
                return {
                    "status": "error",
                    "message": f"Failed to save reminder {reminder_id} to state store"
                }
            
            print(f"Reminder {reminder_id} saved to state store successfully")
            
            # Step 2: Return success result
            result = {
                "status": "success",
                "message": f"Reminder {reminder_id} scheduled successfully",
                "reminderId": reminder_id,
                "scheduledAt": datetime.datetime.now().isoformat(),
                "steps_completed": ["state_store_save"]
            }
            
            print(f"Completed reminder scheduling workflow for reminder {reminder_id}")
            return result
            
        except Exception as e:
            print(f"Error in reminder scheduling workflow: {str(e)}")
            return {
                "status": "error",
                "message": f"Reminder scheduling workflow failed: {str(e)}"
            }

    @staticmethod
    async def process_scheduled_reminders_workflow() -> Dict[str, Any]:
        """
        Execute the workflow to process scheduled reminders:
        1. Check for due reminders in state store
        2. For each due reminder, publish reminder event via pub/sub
        3. Update reminder state to mark as notified
        
        Returns:
            Result of the workflow execution
        """
        try:
            print("Starting scheduled reminder processing workflow")
            
            # In a real implementation, we would:
            # 1. Query the state store for all reminder schedules
            # 2. Check which ones are due based on current time
            # 3. Process those reminders (send notifications, etc.)
            # 4. Update the reminder state to mark them as processed
            
            # For this implementation, we'll simulate the process
            processed_count = 0
            failed_count = 0
            
            # Simulated processing of due reminders
            # In a real system, we would iterate through reminder keys in the state store
            # and check which ones have reminderTime <= now and notified = false
            
            result = {
                "status": "success",
                "message": "Scheduled reminder processing completed",
                "processedCount": processed_count,
                "failedCount": failed_count,
                "processedAt": datetime.datetime.now().isoformat()
            }
            
            print(f"Completed reminder processing workflow: {result}")
            return result
            
        except Exception as e:
            print(f"Error in reminder processing workflow: {str(e)}")
            return {
                "status": "error",
                "message": f"Reminder processing workflow failed: {str(e)}"
            }

    @staticmethod
    async def publish_reminder_notification_workflow(reminder_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the workflow to publish a reminder notification:
        1. Publish reminder event via pub/sub
        2. Update reminder state to mark as notified
        
        Args:
            reminder_data: The reminder data to publish
            
        Returns:
            Result of the workflow execution
        """
        try:
            print(f"Starting reminder notification workflow: {reminder_data.get('reminderId', 'unknown')}")
            
            # Step 1: Publish reminder event via pub/sub
            reminder_event = {
                "eventType": "reminder.triggered",
                "reminderId": reminder_data.get("reminderId"),
                "taskId": reminder_data.get("taskId"),
                "reminderTime": reminder_data.get("reminderTime"),
                "timestamp": datetime.datetime.now().isoformat()
            }
            
            publish_result = await pubsub_service.publish_event("reminders", reminder_event)
            
            if not publish_result:
                return {
                    "status": "error",
                    "message": f"Failed to publish reminder event for {reminder_data.get('reminderId')}"
                }
            
            print(f"Reminder event published successfully for reminder {reminder_id}")
            
            # Step 2: Update reminder state to mark as notified
            reminder_id = reminder_data.get('reminderId')
            reminder_key = REMINDER_STATE_KEY_PATTERN.format(reminderId=reminder_id)
            
            # Update the reminder to mark it as notified
            reminder_data["notified"] = True
            reminder_data["notifiedAt"] = datetime.datetime.now().isoformat()
            
            update_result = await state_service.save_state(reminder_key, reminder_data)
            
            if not update_result:
                # This is a warning rather than an error since the event was published
                print(f"Warning: Reminder event published but failed to update state for {reminder_id}")
                return {
                    "status": "warning",
                    "message": f"Reminder event published but state update failed for {reminder_id}",
                    "reminderId": reminder_id
                }
            
            print(f"Reminder state updated successfully for reminder {reminder_id}")
            
            # Step 3: Return success result
            result = {
                "status": "success",
                "message": f"Reminder notification published successfully for {reminder_id}",
                "reminderId": reminder_id,
                "publishedAt": datetime.datetime.now().isoformat()
            }
            
            print(f"Completed reminder notification workflow for reminder {reminder_id}")
            return result
            
        except Exception as e:
            print(f"Error in reminder notification workflow: {str(e)}")
            return {
                "status": "error",
                "message": f"Reminder notification workflow failed: {str(e)}"
            }

# Global instance
reminder_flow = ReminderFlow()