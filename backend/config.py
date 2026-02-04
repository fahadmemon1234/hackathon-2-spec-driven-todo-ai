"""
Configuration module for the Todo Application backend with Dapr integration
"""

import os
from typing import Optional
from constants import DAPR_HTTP_PORT, DAPR_STATE_STORE_NAME, DAPR_PUBSUB_NAME

# Dapr configuration constants
DAPR_HTTP_PORT = int(os.getenv("DAPR_HTTP_PORT", 3500))
DAPR_GRPC_PORT = int(os.getenv("DAPR_GRPC_PORT", 50001))
DAPR_APP_ID = os.getenv("DAPR_APP_ID", "backend-service")
DAPR_PUBSUB_NAME = os.getenv("DAPR_PUBSUB_NAME", "kafka-pubsub")
DAPR_STATE_STORE_NAME = os.getenv("DAPR_STATE_STORE_NAME", "statestore")

# Component paths
DAPR_COMPONENTS_PATH = os.getenv("DAPR_COMPONENTS_PATH", "./components")

# Timeout configurations
DAPR_HTTP_TIMEOUT_SECONDS = int(os.getenv("DAPR_HTTP_TIMEOUT_SECONDS", 30))

# Logging configuration for Dapr
DAPR_LOG_LEVEL = os.getenv("DAPR_LOG_LEVEL", "info")

# Flag to enable/disable Dapr integration
DAPR_ENABLED = os.getenv("DAPR_ENABLED", "true").lower() == "true"

# Default values (fallback if secrets are not available)
DEFAULT_KAFKA_BROKERS = "localhost:9092"  # Use localhost for local development
DEFAULT_REDIS_HOST = "redis:6379"
DEFAULT_REDIS_PASSWORD = ""

# Configuration values - initially set to defaults, will be updated from secrets
KAFKA_BROKERS = os.getenv("KAFKA_BROKERS", DEFAULT_KAFKA_BROKERS)
REDIS_HOST = os.getenv("REDIS_HOST", DEFAULT_REDIS_HOST)
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", DEFAULT_REDIS_PASSWORD)
DATABASE_URL = os.getenv("DATABASE_URL", "")  # Default to empty, will be loaded from secrets
BETTER_AUTH_SECRET = os.getenv("BETTER_AUTH_SECRET", "")  # Default to empty, will be loaded from secrets

async def load_configuration_from_secrets():
    """
    Load configuration values from Dapr secrets store
    """
    global KAFKA_BROKERS, REDIS_HOST, REDIS_PASSWORD, DATABASE_URL, BETTER_AUTH_SECRET

    try:
        from services.secret_service import secret_service

        # Attempt to load Kafka configuration from secrets
        kafka_brokers = await secret_service.get_secret("kafka_brokers")
        if kafka_brokers:
            KAFKA_BROKERS = kafka_brokers
            print(f"Loaded Kafka brokers from secrets: {KAFKA_BROKERS}")
        else:
            print(f"Using default Kafka brokers: {KAFKA_BROKERS}")

        # Attempt to load Redis host from secrets
        redis_host = await secret_service.get_secret("redis_host")
        if redis_host:
            REDIS_HOST = redis_host
            print(f"Loaded Redis host from secrets: {REDIS_HOST}")
        else:
            print(f"Using default Redis host: {REDIS_HOST}")

        # Attempt to load Redis password from secrets
        redis_password = await secret_service.get_secret("redis_password")
        if redis_password is not None:  # Password can be empty string
            REDIS_PASSWORD = redis_password
            print("Loaded Redis password from secrets")
        else:
            print("Using default Redis password (empty)")

        # Attempt to load database URL from secrets
        database_url = await secret_service.get_secret("DATABASE_URL")
        if database_url:
            DATABASE_URL = database_url
            print("Loaded DATABASE_URL from secrets")
        else:
            print("DATABASE_URL not found in secrets")

        # Attempt to load auth secret from secrets
        auth_secret = await secret_service.get_secret("BETTER_AUTH_SECRET")
        if auth_secret:
            BETTER_AUTH_SECRET = auth_secret
            print("Loaded BETTER_AUTH_SECRET from secrets")
        else:
            print("BETTER_AUTH_SECRET not found in secrets")

    except ImportError:
        # If secret service is not available, use defaults
        print("Secret service not available, using default configuration")
    except Exception as e:
        print(f"Error loading configuration from secrets: {str(e)}")
        print("Using default configuration values")