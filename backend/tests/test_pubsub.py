import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from backend.services.pubsub_service import pubsub_service

@pytest.mark.asyncio
async def test_publish_event_success():
    """Test successful event publishing via Dapr pub/sub"""
    with patch('requests.post') as mock_post:
        # Mock successful response
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        # Test data
        topic = "test-topic"
        data = {"event": "test", "value": 123}
        
        # Execute the function
        result = await pubsub_service.publish_event(topic, data)
        
        # Assertions
        assert result is True
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        assert "http://localhost:3500/v1.0/publish/kafka-pubsub/test-topic" in args[0]
        assert kwargs["headers"]["Content-Type"] == "application/json"


@pytest.mark.asyncio
async def test_publish_event_failure():
    """Test event publishing failure handling"""
    with patch('requests.post') as mock_post:
        # Mock failed response
        mock_response = AsyncMock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response
        
        # Test data
        topic = "test-topic"
        data = {"event": "test", "value": 123}
        
        # Execute the function
        result = await pubsub_service.publish_event(topic, data)
        
        # Assertions
        assert result is False
        mock_post.assert_called_once()


@pytest.mark.asyncio
async def test_publish_task_created():
    """Test publishing task created event"""
    with patch.object(pubsub_service, 'publish_event', new_callable=AsyncMock) as mock_publish:
        mock_publish.return_value = True
        
        # Test data
        task_data = {
            "taskId": "task-123",
            "title": "Test Task",
            "status": "pending"
        }
        
        # Execute the function
        result = await pubsub_service.publish_task_created(task_data)
        
        # Assertions
        assert result is True
        mock_publish.assert_called_once_with("task-events", {
            "eventType": "task.created",
            "task": task_data,
            "timestamp": ""
        })


@pytest.mark.asyncio
async def test_publish_task_updated():
    """Test publishing task updated event"""
    with patch.object(pubsub_service, 'publish_event', new_callable=AsyncMock) as mock_publish:
        mock_publish.return_value = True
        
        # Test data
        task_data = {
            "taskId": "task-123",
            "title": "Updated Task",
            "status": "in-progress"
        }
        
        # Execute the function
        result = await pubsub_service.publish_task_updated(task_data)
        
        # Assertions
        assert result is True
        mock_publish.assert_called_once_with("task-updates", {
            "eventType": "task.updated",
            "task": task_data,
            "timestamp": ""
        })


@pytest.mark.asyncio
async def test_publish_task_deleted():
    """Test publishing task deleted event"""
    with patch.object(pubsub_service, 'publish_event', new_callable=AsyncMock) as mock_publish:
        mock_publish.return_value = True
        
        # Test data
        task_id = "task-123"
        
        # Execute the function
        result = await pubsub_service.publish_task_deleted(task_id)
        
        # Assertions
        assert result is True
        mock_publish.assert_called_once_with("task-events", {
            "eventType": "task.deleted",
            "taskId": task_id,
            "timestamp": ""
        })


@pytest.mark.asyncio
async def test_publish_reminder_event():
    """Test publishing reminder event"""
    with patch.object(pubsub_service, 'publish_event', new_callable=AsyncMock) as mock_publish:
        mock_publish.return_value = True
        
        # Test data
        reminder_data = {
            "reminderId": "reminder-456",
            "taskId": "task-123",
            "reminderTime": "2023-12-31T10:00:00Z"
        }
        
        # Execute the function
        result = await pubsub_service.publish_reminder_event(reminder_data)
        
        # Assertions
        assert result is True
        mock_publish.assert_called_once_with("reminders", {
            "eventType": "reminder.triggered",
            "reminder": reminder_data,
            "timestamp": ""
        })