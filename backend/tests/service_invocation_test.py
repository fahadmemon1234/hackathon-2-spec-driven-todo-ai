import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from backend.handlers.service_invocation import service_invoke

@pytest.mark.asyncio
async def test_service_invoke_health_check():
    """Test service invocation for health check method"""
    # Test data
    method_name = "health-check"
    payload = None
    
    # Execute the function
    result = await service_invoke(method_name, payload)
    
    # Assertions
    assert result["status"] == "healthy"
    assert result["service"] == "backend-service"
    assert "details" in result


@pytest.mark.asyncio
async def test_service_invoke_get_task_summary():
    """Test service invocation for getting task summary"""
    # Test data
    method_name = "get-task-summary"
    payload = {"userId": "user-123"}
    
    # Execute the function
    result = await service_invoke(method_name, payload)
    
    # Assertions
    assert result["status"] == "success"
    assert "user-123" in result["summary"]
    assert "tasks_count" in result
    assert "pending_tasks" in result
    assert "completed_tasks" in result


@pytest.mark.asyncio
async def test_service_invoke_unknown_method():
    """Test service invocation for unknown method"""
    from fastapi import HTTPException
    
    # Test data
    method_name = "unknown-method"
    payload = {"param": "value"}
    
    # Execute the function and expect HTTPException
    with pytest.raises(HTTPException) as exc_info:
        await service_invoke(method_name, payload)
    
    # Assertions
    assert exc_info.value.status_code == 404
    assert "not found" in exc_info.value.detail


@pytest.mark.asyncio
async def test_service_invoke_exception_handling():
    """Test exception handling in service invocation"""
    from fastapi import HTTPException

    # Test data
    method_name = "invalid-method-name-for-testing"
    payload = None

    # Execute the function and expect HTTPException
    with pytest.raises(HTTPException) as exc_info:
        await service_invoke(method_name, payload)

    # Assertions
    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_service_health_endpoint():
    """Test the service health endpoint"""
    from backend.handlers.service_invocation import service_health
    
    # Execute the function
    result = await service_health()
    
    # Assertions
    assert result["status"] == "healthy"
    assert result["service"] == "backend-service"
    assert "checks" in result
    assert "database" in result["checks"]
    assert "redis" in result["checks"]
    assert "kafka" in result["checks"]
    assert "dapr" in result["checks"]


@pytest.mark.asyncio
async def test_service_metadata_endpoint():
    """Test the service metadata endpoint"""
    from backend.handlers.service_invocation import service_metadata
    
    # Execute the function
    result = await service_metadata()
    
    # Assertions
    assert result["serviceId"] == "backend-service"
    assert result["version"] == "1.0.0"
    assert "capabilities" in result
    assert "task-management" in result["capabilities"]
    assert "reminder-scheduling" in result["capabilities"]
    assert "event-publishing" in result["capabilities"]
    assert "state-management" in result["capabilities"]
    
    assert "endpoints" in result
    assert len(result["endpoints"]) > 0
    
    assert "dapr" in result
    assert result["dapr"]["appId"] == "backend-service"