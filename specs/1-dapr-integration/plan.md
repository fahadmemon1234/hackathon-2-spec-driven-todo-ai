# Todo Application – Dapr Integration (Local Docker Compose) Implementation Plan

## Technical Context

Project: Todo Application – Dapr Integration (Local Docker Compose)
Current Status:
- Kafka is running locally via Docker (topics healthy)
- Backend service is running (HTTP port 8000)
- No Dapr sidecars or components implemented yet
- Target: Complete Dapr implementation using Docker Compose (no Kubernetes/Minikube)

Technologies:
- Dapr (Distributed Application Runtime)
- Apache Kafka (Pub/Sub)
- Redis (State Store)
- Docker Compose (Orchestration)
- Python/FastAPI (Backend)

## Constitution Check

Following the project constitution principles:
- Maintain backward compatibility where possible
- Ensure secure handling of secrets
- Implement proper error handling and logging
- Follow clean code practices
- Maintain performance standards
- Ensure proper testing coverage

## Implementation Plan

### PHASE 1: Environment & Infrastructure Setup

**Task 1.1: Install Dapr Runtime**
- Description: Install Dapr CLI and initialize Dapr runtime locally
- Inputs: None
- Actions: 
  - Download and install Dapr CLI
  - Run `dapr init` to install Dapr runtime in standalone mode
  - Verify installation with `dapr --version` and `dapr list`
- Output: Dapr runtime installed and running in standalone mode
- Verification: Run `dapr list` and confirm no runtime errors

**Task 1.2: Update Docker Compose Configuration**
- Description: Modify docker-compose.yml to include Dapr sidecar for backend service
- Inputs: Existing docker-compose.yml, Dapr installed
- Actions:
  - Add Dapr sidecar service to compose file
  - Configure backend service to work with Dapr sidecar
  - Set appropriate ports (Dapr API port 3500)
  - Link services (backend, Kafka, Redis, Dapr)
- Output: Updated docker-compose.yml with Dapr integration
- Verification: Run `docker-compose config` to validate configuration

**Task 1.3: Create Dapr Components Directory**
- Description: Set up directory structure for Dapr component definitions
- Inputs: Project root directory
- Actions:
  - Create `components/` directory in project root
  - Set up subdirectories for different component types if needed
- Output: Components directory structure ready
- Verification: Verify directory exists with `ls -la components/`

**Task 1.4: Configure Redis Connection**
- Description: Ensure Redis is properly configured and accessible
- Inputs: Redis container running via Docker
- Actions:
  - Verify Redis connectivity from backend environment
  - Test Redis connection with basic SET/GET operations
- Output: Confirmed Redis connectivity
- Verification: Connect to Redis and perform basic operations

### PHASE 2: Dapr Pub/Sub Integration

**Task 2.1: Create Kafka Pub/Sub Component Definition**
- Description: Define the Kafka pub/sub component for Dapr
- Inputs: Kafka running on docker network
- Actions:
  - Create `components/pubsub.yaml` file
  - Define kafka-pubsub component with appropriate metadata
  - Configure brokers to point to Kafka container
- Output: Valid pub/sub component definition file
- Verification: Verify component file syntax and configuration

**Task 2.2: Define Kafka Topics**
- Description: Create required Kafka topics for the application
- Inputs: Kafka running, pub/sub component definition
- Actions:
  - Create topics: task-events, reminders, task-updates
  - Verify topics are created and accessible
- Output: Kafka topics created and ready for use
- Verification: List topics using Kafka admin tools

**Task 2.3: Implement Backend Publish Logic**
- Description: Add code to publish messages to Kafka topics via Dapr
- Inputs: Backend service, pub/sub component, Kafka topics
- Actions:
  - Add Dapr client library to backend dependencies
  - Implement publish functions for each topic type
  - Map application events to appropriate topics
- Output: Backend can publish messages to Kafka via Dapr
- Verification: Send test message and verify it appears in Kafka topic

**Task 2.4: Implement Backend Subscribe Logic**
- Description: Add code to subscribe to Kafka topics via Dapr
- Inputs: Backend service, pub/sub component, Kafka topics
- Actions:
  - Implement subscription endpoints in backend
  - Register subscriptions with Dapr
  - Handle incoming messages appropriately
- Output: Backend can receive messages from Kafka via Dapr
- Verification: Publish test message and verify backend receives it

### PHASE 3: Dapr State Store Integration

**Task 3.1: Create Redis State Store Component Definition**
- Description: Define the Redis state store component for Dapr
- Inputs: Redis running on docker network
- Actions:
  - Create `components/statestore.yaml` file
  - Define statestore component with Redis metadata
  - Configure Redis host to point to Redis container
- Output: Valid state store component definition file
- Verification: Verify component file syntax and configuration

**Task 3.2: Design State Key Structure**
- Description: Define the structure for state keys in Redis
- Inputs: Application data model, state store component
- Actions:
  - Define key patterns for different data types
  - Plan for task state: `task:{taskId}`
  - Plan for recurrence metadata: `recurrence:{taskId}`
  - Plan for reminder schedules: `reminder:{reminderId}`
- Output: Documented state key structure
- Verification: Review key structure for consistency and scalability

**Task 3.3: Implement State Operations in Backend**
- Description: Add code to save and retrieve state via Dapr
- Inputs: Backend service, state store component, key structure
- Actions:
  - Implement save state functions using Dapr HTTP API
  - Implement retrieve state functions using Dapr HTTP API
  - Implement delete state functions using Dapr HTTP API
- Output: Backend can perform state operations via Dapr
- Verification: Save and retrieve test data via Dapr state API

### PHASE 4: Dapr Cron Bindings (Reminders)

**Task 4.1: Create Cron Binding Component Definition**
- Description: Define the cron binding component for scheduled tasks
- Inputs: Dapr runtime
- Actions:
  - Create `components/cron-binding.yaml` file
  - Define reminder-cron component with schedule configuration
  - Set up appropriate schedule pattern (e.g., every 5 minutes for testing)
- Output: Valid cron binding component definition file
- Verification: Verify component file syntax and configuration

**Task 4.2: Implement Scheduled Reminder Processing**
- Description: Add backend logic to handle scheduled reminder events
- Inputs: Cron binding component, pub/sub component
- Actions:
  - Create endpoint that Dapr will invoke on schedule
  - Implement logic to check for due reminders
  - Add logic to publish reminder events to Kafka
- Output: Backend responds to cron triggers and processes reminders
- Verification: Trigger cron manually and verify reminder processing

**Task 4.3: End-to-End Reminder Flow Validation**
- Description: Test the complete reminder flow from scheduling to notification
- Inputs: All components implemented
- Actions:
  - Schedule a test reminder
  - Wait for cron to trigger
  - Verify reminder event published to Kafka
  - Verify reminder received by subscribers
- Output: Complete reminder flow working
- Verification: End-to-end test passes successfully

### PHASE 5: Dapr Secrets Integration

**Task 5.1: Create Secrets Component Definition**
- Description: Define the secrets component for local file-based secrets
- Inputs: Dapr runtime
- Actions:
  - Create `components/secrets.yaml` file
  - Define local file secret store component
  - Configure path to secrets file
- Output: Valid secrets component definition file
- Verification: Verify component file syntax and configuration

**Task 5.2: Create Secrets File**
- Description: Create the secrets file with required configuration values
- Inputs: Secrets component definition
- Actions:
  - Create secrets.json file with required secrets
  - Include Kafka brokers, Redis host, and Redis password
  - Ensure proper file permissions and security
- Output: Secure secrets file with configuration values
- Verification: Verify secrets file content and permissions

**Task 5.3: Update Backend to Use Dapr Secrets**
- Description: Modify backend to read configuration from Dapr secrets
- Inputs: Secrets component, secrets file, backend service
- Actions:
  - Replace hardcoded configuration with Dapr secret calls
  - Implement secret retrieval functions using Dapr HTTP API
  - Update configuration loading logic
- Output: Backend retrieves configuration via Dapr secrets
- Verification: Backend starts and operates using secrets from Dapr

### PHASE 6: Dapr Service Invocation

**Task 6.1: Configure Backend App ID**
- Description: Set up the backend service with appropriate Dapr App ID
- Inputs: Dapr sidecar, backend service
- Actions:
  - Configure backend service with App ID "backend-service"
  - Ensure Dapr sidecar is properly linked to backend
- Output: Backend service running with Dapr App ID
- Verification: Verify service can be invoked via Dapr service invocation

**Task 6.2: Implement Service Invocation Endpoints**
- Description: Add endpoints that can be invoked via Dapr service-to-service calls
- Inputs: Backend service, Dapr sidecar
- Actions:
  - Create endpoints that follow Dapr service invocation patterns
  - Implement appropriate request/response handling
- Output: Backend has endpoints accessible via Dapr service invocation
- Verification: Invoke backend endpoints via Dapr service invocation

**Task 6.3: Test Service Invocation Flow**
- Description: Test internal service-to-service calls using Dapr
- Inputs: All service invocation components
- Actions:
  - Make test calls between services using Dapr service invocation
  - Verify request/response handling
- Output: Service invocation working between components
- Verification: Successful service invocation with proper data exchange

### PHASE 7: Testing & Validation

**Task 7.1: Implement Smoke Tests**
- Description: Create basic tests to verify all components are working
- Inputs: All implemented components
- Actions:
  - Create tests that exercise pub/sub functionality
  - Create tests that exercise state store functionality
  - Create tests that exercise cron binding functionality
  - Create tests that exercise secrets functionality
  - Create tests that exercise service invocation functionality
- Output: Comprehensive smoke test suite
- Verification: All smoke tests pass successfully

**Task 7.2: Test Failure Scenarios**
- Description: Verify system behavior under failure conditions
- Inputs: All implemented components
- Actions:
  - Test behavior when Kafka is unavailable
  - Test behavior when Redis is unavailable
  - Test behavior when Dapr sidecar is unavailable
  - Implement appropriate error handling
- Output: System handles failures gracefully
- Verification: Failure scenarios handled appropriately

**Task 7.3: Test Restart Behavior**
- Description: Verify system behavior after restarts
- Inputs: All implemented components
- Actions:
  - Restart individual services and verify functionality
  - Restart Docker Compose stack and verify functionality
  - Verify state persistence across restarts
- Output: System recovers properly after restarts
- Verification: All functionality preserved after restarts

**Task 7.4: Log Verification**
- Description: Verify proper logging across all components
- Inputs: All implemented components
- Actions:
  - Verify Dapr sidecar logs are accessible
  - Verify backend logs include Dapr interactions
  - Verify proper error logging
- Output: Comprehensive logging in place
- Verification: Logs provide sufficient information for debugging

### PHASE 8: Documentation & Readiness

**Task 8.1: Update Local Development Notes**
- Description: Document the Dapr integration for local development
- Inputs: All implemented components
- Actions:
  - Update README with Dapr setup instructions
  - Document component configurations
  - Document common troubleshooting steps
- Output: Updated documentation for local development
- Verification: Documentation is clear and accurate

**Task 8.2: Document Known Limitations**
- Description: Document any known limitations of the current implementation
- Inputs: Implemented system
- Actions:
  - Identify and document any limitations
  - Note areas for future improvement
- Output: Documented known limitations
- Verification: Limitations are clearly communicated

**Task 8.3: Create Ready-for-Cloud Checklist**
- Description: Prepare checklist for eventual cloud migration (without implementing cloud features)
- Inputs: Completed local implementation
- Actions:
  - Create checklist of items needed for cloud deployment
  - Include considerations for production environments
  - Note differences between local and cloud configurations
- Output: Ready-for-cloud checklist
- Verification: Checklist is comprehensive and accurate