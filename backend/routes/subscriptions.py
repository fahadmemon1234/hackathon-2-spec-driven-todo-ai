from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import json

router = APIRouter()

@router.get("/dapr-subscribe")
async def dapr_subscribe():
    """
    Dapr subscription endpoint to define which topics this service wants to subscribe to.
    This tells Dapr which endpoints to call when messages arrive on specific topics.
    """
    subscriptions = [
        {
            "pubsubname": "kafka-pubsub",  # Matches the component name in pubsub.yaml
            "topic": "task-updates",
            "route": "/subscriptions/task-updates"
        },
        {
            "pubsubname": "kafka-pubsub",
            "topic": "reminders",
            "route": "/subscriptions/reminders"
        },
        {
            "pubsubname": "kafka-pubsub",
            "topic": "task-events",
            "route": "/subscriptions/task-events"
        }
    ]
    return subscriptions

@router.post("/subscriptions/task-updates")
async def handle_task_updates(data: Dict[Any, Any]):
    """
    Handle messages from the task-updates topic.
    This endpoint is called by Dapr when a message arrives on the task-updates topic.
    """
    try:
        print(f"Received task update: {json.dumps(data, indent=2)}")
        
        # Process the task update
        # For example, update the task in the database
        # await update_task_in_database(data)
        
        # Return success to acknowledge receipt
        return {"status": "success", "message": "Task update processed"}
    except Exception as e:
        print(f"Error processing task update: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/subscriptions/reminders")
async def handle_reminders(data: Dict[Any, Any]):
    """
    Handle messages from the reminders topic.
    This endpoint is called by Dapr when a message arrives on the reminders topic.
    """
    try:
        print(f"Received reminder: {json.dumps(data, indent=2)}")
        
        # Process the reminder
        # For example, send notification to user
        # await send_reminder_notification(data)
        
        # Return success to acknowledge receipt
        return {"status": "success", "message": "Reminder processed"}
    except Exception as e:
        print(f"Error processing reminder: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/subscriptions/task-events")
async def handle_task_events(data: Dict[Any, Any]):
    """
    Handle messages from the task-events topic.
    This endpoint is called by Dapr when a message arrives on the task-events topic.
    """
    try:
        print(f"Received task event: {json.dumps(data, indent=2)}")
        
        # Process the task event based on event type
        event_type = data.get("eventType", "")
        
        if event_type == "task.created":
            # Handle task created event
            print("Processing task created event")
            # await handle_task_created(data.get("task", {}))
        elif event_type == "task.deleted":
            # Handle task deleted event
            print("Processing task deleted event")
            # await handle_task_deleted(data.get("taskId", ""))
        else:
            print(f"Unknown event type: {event_type}")
        
        # Return success to acknowledge receipt
        return {"status": "success", "message": "Task event processed"}
    except Exception as e:
        print(f"Error processing task event: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))