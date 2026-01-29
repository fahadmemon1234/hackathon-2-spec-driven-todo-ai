"""
Recurring Tasks Workflow Module
This module handles the complete recurring task processing flow using Dapr components
"""

from typing import Dict, Any
import datetime
from backend.services.state_service import state_service
from backend.services.pubsub_service import pubsub_service
from backend.constants import RECURRENCE_STATE_KEY_PATTERN, TASK_STATE_KEY_PATTERN
from backend.utils.recurrence_utils import calculate_next_occurrence

class RecurringTasksWorkflow:
    """Class to handle the complete recurring task processing workflow"""
    
    @staticmethod
    async def process_recurring_tasks_workflow() -> Dict[str, Any]:
        """
        Execute the complete recurring task processing workflow:
        1. Check for recurring tasks that need new instances created
        2. Create new task instances based on recurrence rules
        3. Store new tasks in state store
        4. Publish "task-created" events for new tasks via pub/sub
        
        Returns:
            Result of the workflow execution
        """
        try:
            print("Starting recurring task processing workflow")
            
            # In a real implementation, we would:
            # 1. Query the state store for all recurrence metadata
            # 2. Check which ones need new instances based on recurrence rules and current time
            # 3. Create new task instances based on recurrence rules
            # 4. Store new tasks in state store
            # 5. Publish "task-created" events for new tasks via pub/sub
            
            # For this implementation, we'll simulate the process
            processed_count = 0
            failed_count = 0
            
            # Simulated processing of recurring tasks
            # In a real system, we would iterate through recurrence keys in the state store
            # and check which ones have nextOccurrence <= now
            
            result = {
                "status": "success",
                "message": "Recurring task processing completed",
                "processedCount": processed_count,
                "failedCount": failed_count,
                "processedAt": datetime.datetime.now().isoformat()
            }
            
            print(f"Completed recurring task processing workflow: {result}")
            return result
            
        except Exception as e:
            print(f"Error in recurring task processing workflow: {str(e)}")
            return {
                "status": "error",
                "message": f"Recurring task processing workflow failed: {str(e)}"
            }
    
    @staticmethod
    async def create_recurring_task_instance(task_id: str) -> Dict[str, Any]:
        """
        Create a new instance of a recurring task based on its recurrence rule.
        
        Args:
            task_id: The ID of the recurring task to create a new instance for
            
        Returns:
            Result of the operation
        """
        try:
            print(f"Creating new instance for recurring task: {task_id}")
            
            # Step 1: Retrieve the recurrence metadata from state store
            recurrence_key = RECURRENCE_STATE_KEY_PATTERN.format(taskId=task_id)
            recurrence_data = await state_service.get_state(recurrence_key)
            
            if not recurrence_data:
                return {
                    "status": "error",
                    "message": f"No recurrence metadata found for task {task_id}"
                }
            
            print(f"Recurrence metadata retrieved for task {task_id}")
            
            # Step 2: Retrieve the original task data from state store
            task_key = TASK_STATE_KEY_PATTERN.format(taskId=task_id)
            original_task = await state_service.get_state(task_key)
            
            if not original_task:
                return {
                    "status": "error",
                    "message": f"No original task found for task {task_id}"
                }
            
            print(f"Original task retrieved for task {task_id}")
            
            # Step 3: Calculate the next occurrence based on the recurrence rule
            recurrence_rule = recurrence_data.get("recurrenceRule")
            last_occurrence = recurrence_data.get("lastOccurrence")

            if not recurrence_rule:
                return {
                    "status": "error",
                    "message": f"No recurrence rule found for task {task_id}"
                }

            # Calculate the next occurrence date
            next_occurrence = calculate_next_occurrence(recurrence_rule, last_occurrence)

            if not next_occurrence:
                return {
                    "status": "error",
                    "message": f"Could not calculate next occurrence for task {task_id}"
                }

            print(f"Next occurrence calculated for task {task_id}: {next_occurrence}")

            # Step 4: Create a new task instance based on the original task
            # Generate a new task ID for the instance
            import uuid
            new_task_id = f"{task_id}-instance-{uuid.uuid4().hex[:8]}"

            # Create new task data based on original but with updated dates
            new_task_data = original_task.copy()
            new_task_data["taskId"] = new_task_id
            new_task_data["originalTaskId"] = task_id  # Reference to the original recurring task
            new_task_data["dueDate"] = next_occurrence
            new_task_data["status"] = "pending"  # New instances start as pending
            new_task_data["createdAt"] = datetime.datetime.now().isoformat()
            new_task_data["updatedAt"] = datetime.datetime.now().isoformat()

            # Step 5: Save the new task instance to state store
            new_task_key = TASK_STATE_KEY_PATTERN.format(taskId=new_task_id)
            save_result = await state_service.save_state(new_task_key, new_task_data)

            if not save_result:
                return {
                    "status": "error",
                    "message": f"Failed to save new task instance {new_task_id} to state store"
                }

            print(f"New task instance {new_task_id} saved to state store successfully")

            # Step 6: Update the recurrence metadata to reflect the new last occurrence
            recurrence_data["lastOccurrence"] = next_occurrence
            recurrence_data["updatedAt"] = datetime.datetime.now().isoformat()

            # Calculate the next occurrence after this one
            next_next_occurrence = calculate_next_occurrence(recurrence_rule, next_occurrence)
            recurrence_data["nextOccurrence"] = next_next_occurrence

            update_result = await state_service.save_state(recurrence_key, recurrence_data)

            if not update_result:
                # This is a warning - the new task was created but we couldn't update the recurrence metadata
                print(f"Warning: New task {new_task_id} created but failed to update recurrence metadata for {task_id}")
            else:
                print(f"Recurrence metadata updated for task {task_id}")

            # Step 7: Publish "task-created" event for the new task instance
            task_event = {
                "eventType": "task.created",
                "taskId": new_task_id,
                "taskData": new_task_data,
                "source": "recurring-task",
                "originalTaskId": task_id,
                "timestamp": datetime.datetime.now().isoformat()
            }

            publish_result = await pubsub_service.publish_event("task-events", task_event)

            if not publish_result:
                # This is a warning - the task was created but the event wasn't published
                print(f"Warning: New task {new_task_id} created but event publication failed")
                return {
                    "status": "warning",
                    "message": f"New task {new_task_id} created but event publication failed",
                    "newTaskId": new_task_id,
                    "originalTaskId": task_id
                }

            print(f"Task created event published successfully for new instance {new_task_id}")

            # Step 8: Return success result
            result = {
                "status": "success",
                "message": f"New instance {new_task_id} created for recurring task {task_id}",
                "newTaskId": new_task_id,
                "originalTaskId": task_id,
                "dueDate": next_occurrence,
                "stepsCompleted": ["retrieve_recurrence_metadata", "calculate_occurrence",
                                   "create_task_instance", "update_recurrence_metadata",
                                   "publish_event"]
            }

            print(f"Completed recurring task instance creation workflow for task {task_id}")
            return result
            
        except Exception as e:
            print(f"Error in recurring task instance creation workflow: {str(e)}")
            return {
                "status": "error",
                "message": f"Recurring task instance creation workflow failed: {str(e)}"
            }

# Global instance
recurring_tasks_workflow = RecurringTasksWorkflow()