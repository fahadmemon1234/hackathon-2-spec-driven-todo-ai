"""
Dapr configuration module
This module defines constants and configurations for Dapr integration
"""

# Dapr configuration constants
DAPR_HTTP_PORT = 3500
DAPR_GRPC_PORT = 50001
DAPR_APP_ID = "backend-service"
DAPR_PUBSUB_NAME = "kafka-pubsub"
DAPR_STATE_STORE_NAME = "statestore"

# Component paths
DAPR_COMPONENTS_PATH = "./components"

# Timeout configurations
DAPR_HTTP_TIMEOUT_SECONDS = 30

# Logging configuration for Dapr
DAPR_LOG_LEVEL = "info"