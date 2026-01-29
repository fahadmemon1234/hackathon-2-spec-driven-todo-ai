import json
import os
import requests
from typing import Dict, Any
try:
    from backend.config import DAPR_HTTP_PORT, DAPR_PUBSUB_NAME
except ImportError:
    # Fallback values if backend.config is not available
    DAPR_HTTP_PORT = 3500
    DAPR_PUBSUB_NAME = "kafka-pubsub"

class PubSubService:
    """Service class to handle Dapr pub/sub operations"""
    
    def __init__(self):
        # Use dapr-sidecar service name when running in Docker environment
        # In Docker Compose, services can reach each other via service name
        self.dapr_base_url = f"http://dapr-sidecar:{DAPR_HTTP_PORT}/v1.0"
        
    async def publish_event(self, topic: str, data: Dict[str, Any]) -> bool:
        """
        Publish an event to a specific topic via Dapr
        
        Args:
            topic: The topic name to publish to
            data: The data to publish
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            url = f"{self.dapr_base_url}/publish/{DAPR_PUBSUB_NAME}/{topic}"
            headers = {
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                url,
                headers=headers,
                data=json.dumps(data)
            )
            
            if response.status_code == 200:
                print(f"Successfully published to topic '{topic}'")
                return True
            else:
                print(f"Failed to publish to topic '{topic}'. Status: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"Error publishing to topic '{topic}': {str(e)}")
            return False
    
    async def publish_task_created(self, task_data: Dict[str, Any]) -> bool:
        """Publish a task created event"""
        return await self.publish_event("task-events", {
            "eventType": "task.created",
            "task": task_data,
            "timestamp": task_data.get("createdAt", "")
        })
    
    async def publish_task_updated(self, task_data: Dict[str, Any]) -> bool:
        """Publish a task updated event"""
        return await self.publish_event("task-updates", {
            "eventType": "task.updated",
            "task": task_data,
            "timestamp": task_data.get("updatedAt", "")
        })
    
    async def publish_task_deleted(self, task_id: str) -> bool:
        """Publish a task deleted event"""
        return await self.publish_event("task-events", {
            "eventType": "task.deleted",
            "taskId": task_id,
            "timestamp": ""
        })
    
    async def publish_reminder_event(self, reminder_data: Dict[str, Any]) -> bool:
        """Publish a reminder event"""
        return await self.publish_event("reminders", {
            "eventType": "reminder.triggered",
            "reminder": reminder_data,
            "timestamp": reminder_data.get("reminderTime", "")
        })

# Global instance
pubsub_service = PubSubService()