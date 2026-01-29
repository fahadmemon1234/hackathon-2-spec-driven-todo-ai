import json
import os
import requests
from typing import Any, Optional
try:
    from backend.config import DAPR_HTTP_PORT, DAPR_STATE_STORE_NAME
except ImportError:
    # Fallback values if backend.config is not available
    DAPR_HTTP_PORT = 3500
    DAPR_STATE_STORE_NAME = "statestore"

class StateService:
    """Service class to handle Dapr state store operations"""
    
    def __init__(self):
        # Use dapr-sidecar service name when running in Docker environment
        # In Docker Compose, services can reach each other via service name
        self.dapr_base_url = f"http://dapr-sidecar:{DAPR_HTTP_PORT}/v1.0"
        self.state_store_name = DAPR_STATE_STORE_NAME
        
    async def save_state(self, key: str, data: Any) -> bool:
        """
        Save data to the state store with the given key
        
        Args:
            key: The key to store the data under
            data: The data to store
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            url = f"{self.dapr_base_url}/state/{self.state_store_name}"
            headers = {
                "Content-Type": "application/json"
            }
            
            # Format the request for Dapr state store
            state_item = [{
                "key": key,
                "value": data
            }]
            
            response = requests.post(
                url,
                headers=headers,
                data=json.dumps(state_item)
            )
            
            if response.status_code == 200:
                print(f"Successfully saved state with key '{key}'")
                return True
            else:
                print(f"Failed to save state with key '{key}'. Status: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"Error saving state with key '{key}': {str(e)}")
            return False
    
    async def get_state(self, key: str) -> Optional[Any]:
        """
        Retrieve data from the state store with the given key
        
        Args:
            key: The key to retrieve data for
            
        Returns:
            The stored data if found, None otherwise
        """
        try:
            url = f"{self.dapr_base_url}/state/{self.state_store_name}/{key}"
            headers = {
                "Content-Type": "application/json"
            }

            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                print(f"Successfully retrieved state with key '{key}'")
                return response.json()
            elif response.status_code == 404:
                print(f"State with key '{key}' not found")
                return None
            else:
                print(f"Failed to retrieve state with key '{key}'. Status: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"Error retrieving state with key '{key}': {str(e)}")
            return None
    
    async def delete_state(self, key: str) -> bool:
        """
        Delete data from the state store with the given key
        
        Args:
            key: The key to delete data for
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            url = f"{self.dapr_base_url}/state/{self.state_store_name}/{key}"
            headers = {
                "Content-Type": "application/json"
            }
            
            response = requests.delete(url, headers=headers)
            
            if response.status_code == 204:
                print(f"Successfully deleted state with key '{key}'")
                return True
            elif response.status_code == 404:
                print(f"State with key '{key}' not found, but operation treated as successful")
                return True
            else:
                print(f"Failed to delete state with key '{key}'. Status: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"Error deleting state with key '{key}': {str(e)}")
            return False
    
    async def save_task_state(self, task_id: str, task_data: dict) -> bool:
        """Save task state with the proper key format"""
        key = f"task:{task_id}"
        return await self.save_state(key, task_data)
    
    async def get_task_state(self, task_id: str) -> Optional[dict]:
        """Get task state with the proper key format"""
        key = f"task:{task_id}"
        return await self.get_state(key)
    
    async def save_recurrence_metadata(self, task_id: str, recurrence_data: dict) -> bool:
        """Save recurrence metadata with the proper key format"""
        key = f"recurrence:{task_id}"
        return await self.save_state(key, recurrence_data)
    
    async def get_recurrence_metadata(self, task_id: str) -> Optional[dict]:
        """Get recurrence metadata with the proper key format"""
        key = f"recurrence:{task_id}"
        return await self.get_state(key)
    
    async def save_reminder_schedule(self, reminder_id: str, reminder_data: dict) -> bool:
        """Save reminder schedule with the proper key format"""
        key = f"reminder:{reminder_id}"
        return await self.save_state(key, reminder_data)
    
    async def get_reminder_schedule(self, reminder_id: str) -> Optional[dict]:
        """Get reminder schedule with the proper key format"""
        key = f"reminder:{reminder_id}"
        return await self.get_state(key)

# Global instance
state_service = StateService()