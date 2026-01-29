"""
Task Creation Workflow Module
This module handles the complete task creation flow using Dapr components
"""

from typing import Dict, Any
from backend.services.state_service import state_service
from backend.services.pubsub_service import pubsub_service
from backend.constants import TASK_STATE_KEY_PATTERN

class TaskCreationWorkflow:
    """Class to handle the complete task creation workflow"""
    
    @staticmethod
    async def create_task_workflow(task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the complete task creation workflow:
        1. Store task in state store
        2. Publish "task-created" event via pub/sub
        
        Args:
            task_data: The task data to create
            
        Returns:
            Result of the workflow execution
        """
        try:
            print(f"Starting task creation workflow for task: {task_data.get('id', 'unknown')}")
            
            # Step 1: Store task in state store
            task_id = task_data.get('id') or task_data.get('taskId')
            if not task_id:
                # If no ID provided, we might need to generate one
                # For this implementation, we'll return an error
                return {
                    "status": "error",
                    "message": "Task ID is required for state store operation"
                }
            
            task_key = TASK_STATE_KEY_PATTERN.format(taskId=task_id)
            save_result = await state_service.save_state(task_key, task_data)
            
            if not save_result:
                return {
                    "status": "error",
                    "message": f"Failed to save task {task_id} to state store"
                }
            
            print(f"Task {task_id} saved to state store successfully")
            
            # Step 2: Publish "task-created" event via pub/sub
            task_event = {
                "eventType": "task.created",
                "taskId": task_id,
                "taskData": task_data,
                "timestamp": ""
            }
            
            publish_result = await pubsub_service.publish_event("task-events", task_event)
            
            if not publish_result:
                # Note: We might want to rollback the state store operation
                # if the pub/sub operation fails, depending on requirements
                print(f"Warning: Task {task_id} saved to state store but failed to publish event")
                return {
                    "status": "warning",
                    "message": f"Task {task_id} saved but event publication failed",
                    "taskId": task_id
                }
            
            print(f"Task created event published successfully for task {task_id}")
            
            # Step 3: Return success result
            result = {
                "status": "success",
                "message": f"Task {task_id} created successfully",
                "taskId": task_id,
                "steps_completed": ["state_store_save", "event_publish"]
            }
            
            print(f"Completed task creation workflow for task {task_id}")
            return result
            
        except Exception as e:
            print(f"Error in task creation workflow: {str(e)}")
            return {
                "status": "error",
                "message": f"Task creation workflow failed: {str(e)}"
            }

# Global instance
task_creation_workflow = TaskCreationWorkflow()