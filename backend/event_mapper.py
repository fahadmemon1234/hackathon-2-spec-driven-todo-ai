from typing import Dict, Any, Callable
from backend.services.pubsub_service import pubsub_service

class EventMapper:
    """Maps application events to appropriate Kafka topics via Dapr pub/sub"""
    
    @staticmethod
    async def map_task_created(task_data: Dict[str, Any]):
        """Map task created event to appropriate topic"""
        await pubsub_service.publish_task_created(task_data)
    
    @staticmethod
    async def map_task_updated(task_data: Dict[str, Any]):
        """Map task updated event to appropriate topic"""
        await pubsub_service.publish_task_updated(task_data)
    
    @staticmethod
    async def map_task_deleted(task_id: str):
        """Map task deleted event to appropriate topic"""
        await pubsub_service.publish_task_deleted(task_id)
    
    @staticmethod
    async def map_reminder_triggered(reminder_data: Dict[str, Any]):
        """Map reminder triggered event to appropriate topic"""
        await pubsub_service.publish_reminder_event(reminder_data)
    
    @staticmethod
    async def map_generic_event(event_type: str, data: Dict[str, Any]):
        """Map generic event to appropriate topic based on event type"""
        if event_type == "task.created":
            await pubsub_service.publish_task_created(data)
        elif event_type == "task.updated":
            await pubsub_service.publish_task_updated(data)
        elif event_type == "task.deleted":
            await pubsub_service.publish_task_deleted(data.get("taskId", ""))
        elif event_type == "reminder.triggered":
            await pubsub_service.publish_reminder_event(data)
        else:
            # Default to task-events topic for unknown event types
            await pubsub_service.publish_event("task-events", {
                "eventType": event_type,
                "data": data
            })

# Global instance
event_mapper = EventMapper()