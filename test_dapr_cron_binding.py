import requests
import json

def test_cron_binding_functionality():
    """Test script to verify cron binding functionality"""
    
    # Configuration
    dapr_http_port = 3500
    base_url = f"http://localhost:{dapr_http_port}/v1.0"
    
    print("Testing Dapr Cron Binding functionality...")
    
    # Test 1: Check if cron binding is properly configured
    print("\n1. Checking cron binding configuration...")
    try:
        # Check if the cron binding component is loaded
        response = requests.get(f"{base_url}/v1.0/components")
        
        if response.status_code == 200:
            components = response.json()
            cron_components = [comp for comp in components if 'cron' in comp.get('type', '')]
            print(f"[SUCCESS] Found {len(cron_components)} cron binding component(s)")
            for comp in cron_components:
                print(f"  - {comp.get('name', 'unknown')}: {comp.get('type', 'unknown')}")
        else:
            print(f"[FAILED] Failed to get components list: {response.status_code}")
            
    except Exception as e:
        print(f"[ERROR] Error checking cron binding configuration: {str(e)}")
    
    # Test 2: Check if subscription endpoints are working
    print("\n2. Checking subscription endpoints...")
    try:
        # Check if our subscription endpoints are accessible
        response = requests.get("http://localhost:8000/dapr-subscribe")
        
        if response.status_code == 200:
            subscriptions = response.json()
            print(f"[SUCCESS] Found {len(subscriptions)} subscription(s)")
            for sub in subscriptions:
                print(f"  - Topic: {sub.get('topic', 'unknown')}, Route: {sub.get('route', 'unknown')}")
        else:
            print(f"[FAILED] Failed to get subscriptions: {response.status_code}")
            
    except Exception as e:
        print(f"[ERROR] Error checking subscription endpoints: {str(e)}")
    
    # Test 3: Test manual triggering of reminder processing endpoint
    print("\n3. Testing reminder processing endpoint...")
    try:
        # Call the endpoint that processes scheduled reminders
        response = requests.post("http://localhost:8000/api/process-reminders")

        if response.status_code in [200, 201, 204]:
            print("[SUCCESS] Reminder processing endpoint called successfully")
            if response.text:
                try:
                    result = response.json()
                    print(f"  Response: {json.dumps(result, indent=2)}")
                except:
                    print(f"  Response: {response.text}")
        else:
            print(f"[FAILED] Failed to call reminder processing endpoint: {response.status_code}")
            print(f"  Response: {response.text}")

    except Exception as e:
        print(f"[ERROR] Error calling reminder processing endpoint: {str(e)}")

    # Test 4: Schedule a test reminder
    print("\n4. Scheduling a test reminder...")
    try:
        test_reminder = {
            "reminderId": "test-reminder-123",
            "taskId": "test-task-123",
            "reminderTime": "2026-01-27T22:00:00Z",
            "message": "Test reminder message",
            "notified": False
        }

        response = requests.post("http://localhost:8000/api/schedule-reminder", json=test_reminder)

        if response.status_code in [200, 201]:
            print("[SUCCESS] Test reminder scheduled successfully")
            if response.text:
                try:
                    result = response.json()
                    print(f"  Response: {json.dumps(result, indent=2)}")
                except:
                    print(f"  Response: {response.text}")
        else:
            print(f"[FAILED] Failed to schedule test reminder: {response.status_code}")
            print(f"  Response: {response.text}")

    except Exception as e:
        print(f"[ERROR] Error scheduling test reminder: {str(e)}")
    
    print("\nCron binding functionality test completed!")

if __name__ == "__main__":
    test_cron_binding_functionality()