import json
import datetime
from typing import Dict, Any, Optional
from backend.services.pubsub_service import pubsub_service
from backend.services.state_service import state_service

class ReminderService:
    """Service class to handle reminder-related operations using Dapr"""
    
    async def check_for_due_reminders(self) -> list:
        """
        Check for reminders that are due to be processed.
        
        Returns:
            list: List of due reminders
        """
        try:
            print("Checking for due reminders...")
            
            # In a real implementation, we would query the state store for all reminders
            # and check which ones are due based on their scheduled time.
            # For this implementation, we'll simulate by returning an empty list
            # since we don't have a way to query all reminders in the state store.
            
            # For now, we'll return an empty list - in a real system we would:
            # 1. Iterate through all reminder keys in the state store
            # 2. Check which ones have reminderTime <= now and notified = false
            # 3. Return those reminders for processing
            
            due_reminders = []
            
            print(f"Found {len(due_reminders)} due reminders")
            return due_reminders
            
        except Exception as e:
            print(f"Error checking for due reminders: {str(e)}")
            return []
    
    async def process_due_reminders(self) -> Dict[str, Any]:
        """
        Process all due reminders by checking for them and publishing events.
        
        Returns:
            Dict with processing results
        """
        try:
            print("Processing due reminders...")
            
            # Get all due reminders
            due_reminders = await self.check_for_due_reminders()
            
            processed_count = 0
            failed_count = 0
            
            for reminder in due_reminders:
                try:
                    # Mark the reminder as notified in the state store
                    reminder_id = reminder.get("reminderId")
                    if reminder_id:
                        reminder["notified"] = True
                        reminder["notifiedAt"] = datetime.datetime.now().isoformat()
                        
                        # Update the reminder in the state store
                        reminder_key = f"reminder:{reminder_id}"
                        await state_service.save_state(reminder_key, reminder)
                        
                        # Publish reminder event via pub/sub
                        reminder_event = {
                            "eventType": "reminder.triggered",
                            "reminderId": reminder_id,
                            "taskId": reminder.get("taskId"),
                            "reminderTime": reminder.get("reminderTime"),
                            "timestamp": datetime.datetime.now().isoformat()
                        }
                        
                        success = await pubsub_service.publish_reminder_event(reminder_event)
                        if success:
                            processed_count += 1
                            print(f"Successfully processed reminder: {reminder_id}")
                        else:
                            failed_count += 1
                            print(f"Failed to publish reminder event for: {reminder_id}")
                    else:
                        print(f"Skipping reminder without ID: {reminder}")
                        failed_count += 1
                        
                except Exception as e:
                    print(f"Error processing individual reminder: {str(e)}")
                    failed_count += 1
            
            result = {
                "status": "completed",
                "processed_count": processed_count,
                "failed_count": failed_count,
                "total_checked": len(due_reminders),
                "processed_at": datetime.datetime.now().isoformat()
            }
            
            print(f"Completed reminder processing: {json.dumps(result, indent=2)}")
            return result
            
        except Exception as e:
            print(f"Error processing due reminders: {str(e)}")
            return {
                "status": "error",
                "message": str(e),
                "processed_count": 0,
                "failed_count": 0,
                "total_checked": 0
            }
    
    async def schedule_reminder(self, reminder_data: Dict[str, Any]) -> bool:
        """
        Schedule a new reminder by storing it in the state store.
        
        Args:
            reminder_data: The reminder data to store
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            print(f"Scheduling reminder: {json.dumps(reminder_data, indent=2)}")
            
            reminder_id = reminder_data.get("reminderId")
            if not reminder_id:
                print("Error: Missing reminderId in reminder data")
                return False
            
            # Store the reminder in the state store
            reminder_key = f"reminder:{reminder_id}"
            success = await state_service.save_state(reminder_key, reminder_data)
            
            if success:
                print(f"Successfully scheduled reminder: {reminder_id}")
            else:
                print(f"Failed to schedule reminder: {reminder_id}")
            
            return success
            
        except Exception as e:
            print(f"Error scheduling reminder: {str(e)}")
            return False
    
    async def get_reminder(self, reminder_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific reminder by its ID.
        
        Args:
            reminder_id: The ID of the reminder to retrieve
            
        Returns:
            The reminder data if found, None otherwise
        """
        try:
            print(f"Retrieving reminder: {reminder_id}")
            
            # Get the reminder from the state store
            reminder_key = f"reminder:{reminder_id}"
            reminder_data = await state_service.get_state(reminder_key)
            
            if reminder_data:
                print(f"Retrieved reminder: {reminder_id}")
            else:
                print(f"Reminder not found: {reminder_id}")
            
            return reminder_data
            
        except Exception as e:
            print(f"Error retrieving reminder {reminder_id}: {str(e)}")
            return None
    
    async def publish_reminder_event(self, reminder_data: Dict[str, Any]) -> bool:
        """
        Publish a reminder event to the appropriate Kafka topic via Dapr pub/sub.
        
        Args:
            reminder_data: The reminder event data to publish
            
        Returns:
            bool: True if published successfully, False otherwise
        """
        try:
            print(f"Publishing reminder event: {json.dumps(reminder_data, indent=2)}")
            
            # Publish to the reminders topic
            success = await pubsub_service.publish_event("reminders", reminder_data)
            
            if success:
                print("Successfully published reminder event")
            else:
                print("Failed to publish reminder event")
            
            return success
            
        except Exception as e:
            print(f"Error publishing reminder event: {str(e)}")
            return False

# Global instance
reminder_service = ReminderService()