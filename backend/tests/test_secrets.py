import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from backend.services.secret_service import secret_service

@pytest.mark.asyncio
async def test_get_secret_success():
    """Test successful secret retrieval via Dapr secrets API"""
    with patch('requests.get') as mock_get:
        # Mock successful response
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "kafka_brokers": "kafka:9092",
            "redis_host": "redis:6379",
            "redis_password": ""
        }
        mock_get.return_value = mock_response
        
        # Test data
        secret_key = "kafka_brokers"
        
        # Execute the function
        result = await secret_service.get_secret(secret_key)
        
        # Assertions
        assert result == "kafka:9092"
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert "http://localhost:3500/v1.0/secrets/local-secret-store/kafka_brokers" in args[0]


@pytest.mark.asyncio
async def test_get_secret_not_found():
    """Test secret retrieval when secret doesn't exist"""
    with patch('requests.get') as mock_get:
        # Mock 404 response
        mock_response = AsyncMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        # Test data
        secret_key = "non-existent-secret"
        
        # Execute the function
        result = await secret_service.get_secret(secret_key)
        
        # Assertions
        assert result is None
        mock_get.assert_called_once()


@pytest.mark.asyncio
async def test_get_secret_server_error():
    """Test secret retrieval when server returns error"""
    with patch('requests.get') as mock_get:
        # Mock server error response
        mock_response = AsyncMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_get.return_value = mock_response
        
        # Test data
        secret_key = "some-secret"
        
        # Execute the function
        result = await secret_service.get_secret(secret_key)
        
        # Assertions
        assert result is None
        mock_get.assert_called_once()


@pytest.mark.asyncio
async def test_get_multiple_secrets():
    """Test retrieval of multiple secrets"""
    with patch.object(secret_service, 'get_secret', new_callable=AsyncMock) as mock_get_secret:
        # Mock return values for different secrets
        async def async_side_effect(key):
            secrets_map = {
                "kafka_brokers": "kafka:9092",
                "redis_host": "redis:6379",
                "redis_password": ""
            }
            return secrets_map.get(key)
        
        mock_get_secret.side_effect = async_side_effect
        
        # Test data
        keys = ["kafka_brokers", "redis_host", "redis_password", "nonexistent"]
        
        # Execute the function
        result = await secret_service.get_multiple_secrets(keys)
        
        # Assertions
        expected_result = {
            "kafka_brokers": "kafka:9092",
            "redis_host": "redis:6379",
            "redis_password": ""
        }
        assert result == expected_result
        assert mock_get_secret.call_count == 4  # Called for each key


@pytest.mark.asyncio
async def test_get_secret_exception_handling():
    """Test exception handling in secret retrieval"""
    with patch('requests.get', side_effect=Exception("Network error")):
        # Test data
        secret_key = "some-secret"
        
        # Execute the function
        result = await secret_service.get_secret(secret_key)
        
        # Assertions
        assert result is None


@pytest.mark.asyncio
async def test_load_configuration_from_secrets_success():
    """Test successful loading of configuration from secrets"""
    from backend.config import load_configuration_from_secrets
    
    with patch('backend.services.secret_service.secret_service.get_secret') as mock_get_secret:
        # Mock return values for configuration secrets
        async def async_side_effect(key):
            config_values = {
                "kafka_brokers": "kafka:9092",
                "redis_host": "redis:6379",
                "redis_password": "password123"
            }
            return config_values.get(key)
        
        mock_get_secret.side_effect = async_side_effect
        
        # Execute the function
        await load_configuration_from_secrets()
        
        # Verify that the secrets were accessed
        calls = [call("kafka_brokers"), call("redis_host"), call("redis_password")]
        mock_get_secret.assert_has_calls(calls, any_order=True)


@pytest.mark.asyncio
async def test_load_configuration_from_secrets_with_defaults():
    """Test loading configuration when some secrets are missing (should use defaults)"""
    from backend.config import load_configuration_from_secrets, DEFAULT_KAFKA_BROKERS, DEFAULT_REDIS_HOST
    
    with patch('backend.services.secret_service.secret_service.get_secret') as mock_get_secret, \
         patch('backend.config.KAFKA_BROKERS', DEFAULT_KAFKA_BROKERS), \
         patch('backend.config.REDIS_HOST', DEFAULT_REDIS_HOST), \
         patch('backend.config.REDIS_PASSWORD', ''):
        
        # Mock return values - some secrets missing
        async def async_side_effect(key):
            if key == "kafka_brokers":
                return "custom-kafka:9092"
            elif key == "redis_host":
                return None  # Missing secret
            elif key == "redis_password":
                return ""  # Empty password
            return None
        
        mock_get_secret.side_effect = async_side_effect
        
        # Execute the function
        await load_configuration_from_secrets()
        
        # Verify that secrets were accessed
        calls = [call("kafka_brokers"), call("redis_host"), call("redis_password")]
        mock_get_secret.assert_has_calls(calls, any_order=True)


@pytest.mark.asyncio
async def test_load_configuration_from_secrets_import_error():
    """Test loading configuration when secret service is not available"""
    from backend.config import load_configuration_from_secrets
    
    # Temporarily remove the import to simulate ImportError
    import sys
    original_backend = sys.modules.get('backend.services.secret_service')
    sys.modules['backend.services.secret_service'] = None
    
    try:
        # Execute the function (should handle ImportError gracefully)
        await load_configuration_from_secrets()
        # If we reach this point, the function handled the error correctly
        assert True  # Just to confirm the test passed
    except Exception:
        # If an exception occurs, it means error handling didn't work as expected
        assert False, "Exception was not handled properly"
    finally:
        # Restore the original module
        if original_backend:
            sys.modules['backend.services.secret_service'] = original_backend


@pytest.mark.asyncio
async def test_load_configuration_from_secrets_general_error():
    """Test loading configuration when general error occurs"""
    from backend.config import load_configuration_from_secrets
    
    with patch('backend.services.secret_service.secret_service.get_secret', side_effect=Exception("General error")):
        # Execute the function (should handle general error gracefully)
        await load_configuration_from_secrets()
        # If we reach this point, the function handled the error correctly
        assert True  # Just to confirm the test passed