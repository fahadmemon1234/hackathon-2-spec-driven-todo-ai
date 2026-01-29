import os
import requests
import json
from typing import Dict, Any, Optional
from backend.config import DAPR_HTTP_PORT

class SecretService:
    """Service class to handle Dapr secret store operations"""
    
    def __init__(self):
        # Use dapr-sidecar service name when running in Docker environment
        # In Docker Compose, services can reach each other via service name
        self.dapr_base_url = f"http://dapr-sidecar:{DAPR_HTTP_PORT}/v1.0"
        self.secret_store_name = "local-secret-store"
        
    async def get_secret(self, key: str) -> Optional[str]:
        """
        Retrieve a secret from the Dapr secret store
        
        Args:
            key: The key of the secret to retrieve
            
        Returns:
            The secret value if found, None otherwise
        """
        try:
            url = f"{self.dapr_base_url}/secrets/{self.secret_store_name}/{key}"
            headers = {
                "Content-Type": "application/json"
            }
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                secret_response = response.json()
                # The response contains a dictionary where the key is the secret name
                # and the value is the secret value
                secret_value = secret_response.get(key)
                if secret_value is not None:
                    print(f"Successfully retrieved secret with key '{key}'")
                    return secret_value
                else:
                    print(f"Secret with key '{key}' not found in response")
                    return None
            elif response.status_code == 404:
                print(f"Secret with key '{key}' not found")
                return None
            else:
                print(f"Failed to retrieve secret with key '{key}'. Status: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"Error retrieving secret with key '{key}': {str(e)}")
            return None
    
    async def get_multiple_secrets(self, keys: list) -> Dict[str, str]:
        """
        Retrieve multiple secrets from the Dapr secret store
        
        Args:
            keys: List of secret keys to retrieve
            
        Returns:
            Dictionary mapping keys to their values
        """
        secrets = {}
        for key in keys:
            value = await self.get_secret(key)
            if value is not None:
                secrets[key] = value
        return secrets

# Global instance
secret_service = SecretService()