# Kafka Local Setup - Implementation Tasks (sp.tasks)

## 1. Overview
This document outlines the implementation tasks for setting up a local Kafka development environment using Docker Compose with a single broker and Zookeeper. The setup resolves the common Docker listener/advertised.listeners mismatch issue by configuring dual listeners for internal and external access.

## 2. Phase 1: Setup
Initialize the project structure and create the Docker Compose configuration.

- [X] T001 Create project directory structure for Kafka setup
- [X] T002 Create docker-compose.yml file with initial configuration
- [X] T003 Install required dependencies (Docker, Docker Compose, Python)

## 3. Phase 2: Foundational
Configure the foundational elements of the Kafka setup.

- [X] T004 Configure Zookeeper service in docker-compose.yml
- [X] T005 Configure Kafka service with dual listeners in docker-compose.yml
- [X] T006 Set environment variables for Kafka configuration in docker-compose.yml
- [X] T007 Configure network settings for container communication in docker-compose.yml

## 4. Phase 3: [US1] Start Kafka Stack
Implement the functionality to start the Kafka stack reliably.

- [X] T008 [US1] Implement docker-compose up command execution
- [X] T009 [US1] Verify container startup success
- [X] T010 [US1] Monitor logs for successful Kafka startup

## 5. Phase 4: [US2] Topic Creation
Implement the functionality to create required Kafka topics.

- [X] T011 [US2] Create task-events topic with 3 partitions and replication factor 1
- [X] T012 [US2] Create reminders topic with 1 partition and replication factor 1
- [X] T013 [US2] Create task-updates topic with 3 partitions and replication factor 1
- [X] T014 [US2] Verify all topics exist with correct configurations

## 6. Phase 5: [US3] Connectivity Test
Implement the functionality to test Kafka connectivity from the host.

- [X] T015 [US3] Install kafka-python library for connectivity testing
- [X] T016 [US3] Create Python producer script to send test message to task-events
- [X] T017 [US3] Create Python consumer script to receive test message from task-events
- [X] T018 [US3] Execute end-to-end connectivity test between producer and consumer

## 7. Phase 6: Polish & Cross-Cutting Concerns
Finalize the implementation with cleanup and documentation.

- [X] T019 Document the Kafka setup process and usage instructions
- [X] T020 Create cleanup script for stopping and removing containers
- [X] T021 Verify no ERROR or FATAL messages in Kafka logs related to listeners or connections
- [X] T022 Update README with troubleshooting tips for common issues

## 8. Dependencies & Ordering
- T001 → T002: Project structure must exist before creating docker-compose.yml
- T002 → T004: Docker Compose file must exist before configuring Zookeeper
- T004 → T005: Zookeeper must be configured before Kafka
- T005 → T006: Kafka service must be defined before setting environment variables
- T006 → T007: Environment variables must be set before network configuration
- T007 → T008: Network must be configured before starting containers
- T008 → T009: Containers must be started before verifying startup
- T009 → T010: Startup must be verified before monitoring logs
- T010 → T011: Kafka must be running before creating topics
- T011 → T012: task-events topic must be created before reminders topic
- T012 → T013: reminders topic must be created before task-updates topic
- T013 → T014: All topics must exist before verification
- T014 → T015: Topics must be verified before installing kafka-python
- T015 → T016: kafka-python must be installed before creating producer script
- T016 → T017: Producer must be created before consumer script
- T017 → T018: Consumer must be created before executing connectivity test
- T018 → T021: Connectivity test must pass before verifying logs
- T021 → T019: Logs must be clean before documenting setup
- T019 → T020: Documentation must exist before creating cleanup script
- T020 → T022: Cleanup script must exist before final verification

## 9. Parallel Execution Opportunities
- T004 and T005 can run in parallel: Configuring Zookeeper and Kafka services
- T011, T012, and T013 can run in parallel: Creating different topics simultaneously
- T016 and T017 can run in parallel: Creating producer and consumer scripts simultaneously

## 10. Implementation Strategy
- MVP Scope: Focus on US1 (starting Kafka stack) and US2 (creating topics) for initial implementation
- Incremental Delivery:
  1. Phase 1-2: Complete setup and foundational configuration
  2. Phase 3: Implement and verify Kafka stack startup
  3. Phase 4: Implement and verify topic creation
  4. Phase 5: Implement and verify connectivity testing
  5. Phase 6: Complete documentation and cleanup