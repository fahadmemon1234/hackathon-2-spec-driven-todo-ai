import requests
import json

def test_pubsub_functionality():
    """Test script to verify pub/sub functionality via Dapr API"""

    # Configuration
    dapr_http_port = 3500
    base_url = f"http://localhost:{dapr_http_port}/v1.0"

    print("Testing Dapr Pub/Sub functionality...")

    # Test 1: Send a test message to task-events topic
    print("\n1. Publishing test message to task-events topic...")
    topic_name = "task-events"
    test_data = {
        "taskId": "test-123",
        "eventType": "task.created",
        "title": "Test Task",
        "status": "pending",
        "timestamp": ""
    }

    try:
        url = f"{base_url}/publish/kafka-pubsub/{topic_name}"
        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(url, headers=headers, data=json.dumps(test_data))

        if response.status_code == 200:
            print(f"[SUCCESS] Successfully published message to {topic_name} topic")
            print(f"  Response: {response.status_code}")
        else:
            print(f"[FAILED] Failed to publish message to {topic_name} topic")
            print(f"  Response: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"[ERROR] Error publishing message: {str(e)}")

    # Test 2: Send a test message to reminders topic
    print("\n2. Publishing test message to reminders topic...")
    topic_name = "reminders"
    test_data = {
        "reminderId": "reminder-test-456",
        "taskId": "task-123",
        "reminderTime": "2026-01-27T21:00:00Z",
        "message": "Test reminder message",
        "timestamp": ""
    }

    try:
        url = f"{base_url}/publish/kafka-pubsub/{topic_name}"
        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(url, headers=headers, data=json.dumps(test_data))

        if response.status_code == 200:
            print(f"[SUCCESS] Successfully published message to {topic_name} topic")
            print(f"  Response: {response.status_code}")
        else:
            print(f"[FAILED] Failed to publish message to {topic_name} topic")
            print(f"  Response: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"[ERROR] Error publishing message: {str(e)}")

    # Test 3: Send a test message to task-updates topic
    print("\n3. Publishing test message to task-updates topic...")
    topic_name = "task-updates"
    test_data = {
        "taskId": "task-123",
        "eventType": "task.updated",
        "field": "status",
        "oldValue": "pending",
        "newValue": "in-progress",
        "timestamp": ""
    }

    try:
        url = f"{base_url}/publish/kafka-pubsub/{topic_name}"
        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(url, headers=headers, data=json.dumps(test_data))

        if response.status_code == 200:
            print(f"[SUCCESS] Successfully published message to {topic_name} topic")
            print(f"  Response: {response.status_code}")
        else:
            print(f"[FAILED] Failed to publish message to {topic_name} topic")
            print(f"  Response: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"[ERROR] Error publishing message: {str(e)}")

    print("\nPub/Sub functionality test completed!")

if __name__ == "__main__":
    test_pubsub_functionality()