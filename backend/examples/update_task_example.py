"""
Example code for updating an existing task in the database
"""

from sqlmodel import Session
from datetime import datetime
from db import engine
from models import Task
from routes.tasks import TaskUpdate


def update_existing_task_example():
    """
    Example of how to update an existing task in the database
    """
    # Create a database session
    with Session(engine) as session:
        # Get the task you want to update (assuming task ID 1 exists)
        task_id = 1  # Change this to the actual task ID you want to update
        task = session.get(Task, task_id)
        
        if task:
            # Create an update object with the fields you want to change
            task_update_data = TaskUpdate(
                title="Updated Task Title",
                description="This is the updated description",
                completed=True,
                priority="high",
                category="work",
                tags=["important", "updated", "example"],
                due_date=datetime(2024, 12, 31, 15, 30),  # Year, Month, Day, Hour, Minute
                is_recurring=False,
                recurrence_rule=None,
                reminder_time=datetime(2024, 12, 31, 14, 30),  # 1 hour before due
                reminder_type="email",
                reminder_offset=60  # 60 minutes before due date
            )
            
            # Update the task fields
            if task_update_data.title is not None:
                task.title = task_update_data.title
            if task_update_data.description is not None:
                task.description = task_update_data.description
            if task_update_data.completed is not None:
                task.completed = task_update_data.completed
            if task_update_data.priority is not None:
                task.priority = task_update_data.priority
            if task_update_data.category is not None:
                task.category = task_update_data.category
            if task_update_data.tags is not None:
                task.tags = task_update_data.tags
            if task_update_data.due_date is not None:
                task.due_date = task_update_data.due_date
            if task_update_data.is_recurring is not None:
                task.is_recurring = task_update_data.is_recurring
            if task_update_data.recurrence_rule is not None:
                task.recurrence_rule = task_update_data.recurrence_rule
            if task_update_data.reminder_time is not None:
                task.reminder_time = task_update_data.reminder_time
            if task_update_data.reminder_type is not None:
                task.reminder_type = task_update_data.reminder_type
            if task_update_data.reminder_offset is not None:
                task.reminder_offset = task_update_data.reminder_offset
            
            # Update the updated_at timestamp
            task.updated_at = datetime.utcnow()
            
            # If it's a recurring task, calculate the next occurrence
            if task.is_recurring and task.recurrence_rule:
                from utils.recurrence_utils import calculate_next_occurrence
                if task.due_date:
                    next_occurrence = calculate_next_occurrence(task.recurrence_rule, task.due_date)
                    task.next_occurrence = next_occurrence
            
            # Commit the changes to the database
            session.add(task)
            session.commit()
            session.refresh(task)
            
            print(f"Task updated successfully: {task.title}")
            print(f"Updated at: {task.updated_at}")
        else:
            print(f"Task with ID {task_id} not found")


def update_task_by_api_call_example():
    """
    Example of how the API endpoint would be called
    This is just for demonstration - you would typically make this request from a client
    """
    import requests
    import json
    
    # Example API call to update a task
    task_id = 1  # Change this to the actual task ID
    api_url = "http://localhost:8000/api/tasks/"
    headers = {
        "Authorization": "Bearer YOUR_JWT_TOKEN_HERE",  # Replace with actual JWT token
        "Content-Type": "application/json"
    }
    
    # Data to update
    update_data = {
        "title": "Updated Task Title via API",
        "description": "This task was updated via API call",
        "completed": False,
        "priority": "medium",
        "category": "personal",
        "tags": ["api", "update", "example"],
        "due_date": "2024-12-31T15:30:00",
        "is_recurring": True,
        "recurrence_rule": "DAILY",
        "reminder_time": "2024-12-31T14:30:00",
        "reminder_type": "email",
        "reminder_offset": 60
    }
    
    # Make the API call
    # response = requests.put(
    #     f"{api_url}{task_id}",
    #     headers=headers,
    #     data=json.dumps(update_data)
    # )
    #
    # if response.status_code == 200:
    #     updated_task = response.json()
    #     print("Task updated successfully via API:")
    #     print(updated_task)
    # else:
    #     print(f"Failed to update task: {response.status_code} - {response.text}")
    
    print("API call example prepared. Uncomment the code above to execute.")
    print("Make sure to replace 'YOUR_JWT_TOKEN_HERE' with a valid JWT token.")


if __name__ == "__main__":
    print("Running task update examples...")
    update_existing_task_example()
    update_task_by_api_call_example()