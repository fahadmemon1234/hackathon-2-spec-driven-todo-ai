import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from backend.services.state_service import state_service

@pytest.mark.asyncio
async def test_save_state_success():
    """Test successful state saving via Dapr state store"""
    with patch('requests.post') as mock_post:
        # Mock successful response
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        # Test data
        key = "test-key"
        data = {"value": "test-data", "status": "active"}
        
        # Execute the function
        result = await state_service.save_state(key, data)
        
        # Assertions
        assert result is True
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        assert "http://localhost:3500/v1.0/state/statestore" in args[0]
        assert kwargs["headers"]["Content-Type"] == "application/json"
        
        # Check that the request body contains the correct state item
        import json
        request_body = json.loads(kwargs["data"])
        assert len(request_body) == 1
        assert request_body[0]["key"] == key
        assert request_body[0]["value"] == data


@pytest.mark.asyncio
async def test_save_state_failure():
    """Test state saving failure handling"""
    with patch('requests.post') as mock_post:
        # Mock failed response
        mock_response = AsyncMock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response
        
        # Test data
        key = "test-key"
        data = {"value": "test-data"}
        
        # Execute the function
        result = await state_service.save_state(key, data)
        
        # Assertions
        assert result is False
        mock_post.assert_called_once()


@pytest.mark.asyncio
async def test_get_state_success():
    """Test successful state retrieval"""
    with patch('requests.get') as mock_get:
        # Mock successful response with data
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"value": "test-data", "version": "1.0"}
        mock_get.return_value = mock_response
        
        # Test data
        key = "test-key"
        
        # Execute the function
        result = await state_service.get_state(key)
        
        # Assertions
        assert result == {"value": "test-data", "version": "1.0"}
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert "http://localhost:3500/v1.0/state/statestore/test-key" in args[0]


@pytest.mark.asyncio
async def test_get_state_not_found():
    """Test state retrieval when key doesn't exist"""
    with patch('requests.get') as mock_get:
        # Mock 404 response
        mock_response = AsyncMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        # Test data
        key = "non-existent-key"
        
        # Execute the function
        result = await state_service.get_state(key)
        
        # Assertions
        assert result is None
        mock_get.assert_called_once()


@pytest.mark.asyncio
async def test_delete_state_success():
    """Test successful state deletion"""
    with patch('requests.delete') as mock_delete:
        # Mock successful response
        mock_response = AsyncMock()
        mock_response.status_code = 204  # No content for successful delete
        mock_delete.return_value = mock_response
        
        # Test data
        key = "test-key-to-delete"
        
        # Execute the function
        result = await state_service.delete_state(key)
        
        # Assertions
        assert result is True
        mock_delete.assert_called_once()
        args, kwargs = mock_delete.call_args
        assert "http://localhost:3500/v1.0/state/statestore/test-key-to-delete" in args[0]


@pytest.mark.asyncio
async def test_delete_state_not_found():
    """Test state deletion when key doesn't exist (should still return True)"""
    with patch('requests.delete') as mock_delete:
        # Mock 404 response - in Dapr, deleting a non-existent key is treated as success
        mock_response = AsyncMock()
        mock_response.status_code = 404
        mock_delete.return_value = mock_response
        
        # Test data
        key = "non-existent-key"
        
        # Execute the function
        result = await state_service.delete_state(key)
        
        # Assertions
        assert result is True  # Dapr treats deletion of non-existent keys as success
        mock_delete.assert_called_once()


@pytest.mark.asyncio
async def test_save_task_state():
    """Test saving task state with proper key pattern"""
    with patch.object(state_service, 'save_state', new_callable=AsyncMock) as mock_save:
        mock_save.return_value = True
        
        # Test data
        task_id = "task-123"
        task_data = {
            "taskId": task_id,
            "title": "Test Task",
            "status": "pending"
        }
        
        # Execute the function
        result = await state_service.save_task_state(task_id, task_data)
        
        # Assertions
        assert result is True
        mock_save.assert_called_once_with(f"task:{task_id}", task_data)


@pytest.mark.asyncio
async def test_get_task_state():
    """Test retrieving task state with proper key pattern"""
    with patch.object(state_service, 'get_state', new_callable=AsyncMock) as mock_get:
        expected_task_data = {
            "taskId": "task-123",
            "title": "Test Task",
            "status": "pending"
        }
        mock_get.return_value = expected_task_data
        
        # Test data
        task_id = "task-123"
        
        # Execute the function
        result = await state_service.get_task_state(task_id)
        
        # Assertions
        assert result == expected_task_data
        mock_get.assert_called_once_with(f"task:{task_id}")


@pytest.mark.asyncio
async def test_save_reminder_schedule():
    """Test saving reminder schedule with proper key pattern"""
    with patch.object(state_service, 'save_state', new_callable=AsyncMock) as mock_save:
        mock_save.return_value = True
        
        # Test data
        reminder_id = "reminder-456"
        reminder_data = {
            "reminderId": reminder_id,
            "taskId": "task-123",
            "reminderTime": "2023-12-31T10:00:00Z",
            "notified": False
        }
        
        # Execute the function
        result = await state_service.save_reminder_schedule(reminder_id, reminder_data)
        
        # Assertions
        assert result is True
        mock_save.assert_called_once_with(f"reminder:{reminder_id}", reminder_data)