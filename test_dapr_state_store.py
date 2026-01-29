import requests
import json

def test_state_store_functionality():
    """Test script to verify state store functionality via Dapr API"""
    
    # Configuration
    dapr_http_port = 3500
    base_url = f"http://localhost:{dapr_http_port}/v1.0"
    state_store_name = "statestore"
    
    print("Testing Dapr State Store functionality...")
    
    # Test 1: Save test data to state store
    print("\n1. Saving test data to state store...")
    key = "task:test-123"
    test_data = {
        "taskId": "test-123",
        "title": "Test Task",
        "status": "pending",
        "priority": "high",
        "createdAt": "2026-01-27T21:00:00Z"
    }
    
    try:
        url = f"{base_url}/state/{state_store_name}"
        headers = {
            "Content-Type": "application/json"
        }
        
        # Format the request for Dapr state store (array of state items)
        state_items = [{
            "key": key,
            "value": test_data
        }]
        
        response = requests.post(url, headers=headers, data=json.dumps(state_items))
        
        if response.status_code == 200:
            print(f"[SUCCESS] Successfully saved data with key '{key}' to state store")
        else:
            print(f"[FAILED] Failed to save data with key '{key}' to state store")
            print(f"  Response: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"[ERROR] Error saving data to state store: {str(e)}")
    
    # Test 2: Retrieve the saved test data from state store
    print("\n2. Retrieving test data from state store...")
    
    try:
        url = f"{base_url}/state/{state_store_name}/{key}"
        headers = {
            "Content-Type": "application/json"
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            retrieved_data = response.json()
            print(f"[SUCCESS] Successfully retrieved data with key '{key}' from state store")
            print(f"  Retrieved data: {json.dumps(retrieved_data, indent=2)}")
        elif response.status_code == 404:
            print(f"[INFO] No data found with key '{key}' in state store")
        else:
            print(f"[FAILED] Failed to retrieve data with key '{key}' from state store")
            print(f"  Response: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"[ERROR] Error retrieving data from state store: {str(e)}")
    
    # Test 3: Save recurrence metadata
    print("\n3. Saving recurrence metadata to state store...")
    recurrence_key = "recurrence:test-123"
    recurrence_data = {
        "taskId": "test-123",
        "recurrenceRule": "FREQ=DAILY;INTERVAL=1",
        "lastOccurrence": "2026-01-26T10:00:00Z",
        "nextOccurrence": "2026-01-27T10:00:00Z",
        "endDate": None
    }
    
    try:
        url = f"{base_url}/state/{state_store_name}"
        headers = {
            "Content-Type": "application/json"
        }
        
        # Format the request for Dapr state store
        state_items = [{
            "key": recurrence_key,
            "value": recurrence_data
        }]
        
        response = requests.post(url, headers=headers, data=json.dumps(state_items))
        
        if response.status_code == 200:
            print(f"[SUCCESS] Successfully saved recurrence data with key '{recurrence_key}' to state store")
        else:
            print(f"[FAILED] Failed to save recurrence data with key '{recurrence_key}' to state store")
            print(f"  Response: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"[ERROR] Error saving recurrence data to state store: {str(e)}")
    
    # Test 4: Retrieve the saved recurrence metadata
    print("\n4. Retrieving recurrence metadata from state store...")
    
    try:
        url = f"{base_url}/state/{state_store_name}/{recurrence_key}"
        headers = {
            "Content-Type": "application/json"
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            retrieved_data = response.json()
            print(f"[SUCCESS] Successfully retrieved recurrence data with key '{recurrence_key}' from state store")
            print(f"  Retrieved data: {json.dumps(retrieved_data, indent=2)}")
        elif response.status_code == 404:
            print(f"[INFO] No recurrence data found with key '{recurrence_key}' in state store")
        else:
            print(f"[FAILED] Failed to retrieve recurrence data with key '{recurrence_key}' from state store")
            print(f"  Response: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"[ERROR] Error retrieving recurrence data from state store: {str(e)}")
    
    print("\nState store functionality test completed!")

if __name__ == "__main__":
    test_state_store_functionality()