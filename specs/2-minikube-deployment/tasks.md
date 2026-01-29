# Local Deployment – Minikube Implementation Tasks

## Feature Overview

This feature implements a local Kubernetes-based deployment using Minikube for the Todo Application with Dapr integration. The goal is to provide an alternative deployment option that validates Kubernetes orchestration, Dapr sidecar behavior, and service networking in a cluster-like environment. This deployment is optional and only required for Kubernetes practice, Dapr-on-Kubernetes validation, and cloud deployment preparation.

## Implementation Strategy

- **MVP First**: Start with basic Kubernetes deployment of existing services
- **Incremental Delivery**: Add Dapr integration, then advanced features
- **Independent Testing**: Each phase should be testable in isolation
- **Parallel Execution**: Where possible, tasks are marked with [P] for parallel execution

## Dependencies

- Docker Desktop must be installed and running
- Application must be working in Docker Compose environment
- Dapr CLI should be available for verification

## Parallel Execution Examples

- Manifest creation for different services can be done in parallel
- Dapr component deployments can be done in parallel after Dapr installation
- Verification tasks can be done in parallel after deployment

---

## Phase 1: Setup (Project Initialization)

- [x] T001 Create k8s directory for Kubernetes manifests in k8s/
- [x] T002 Verify Minikube installation with `minikube version` command
- [x] T003 Verify kubectl installation with `kubectl version` command
- [x] T004 Create namespace definition for the application in k8s/namespace.yaml
- [x] T005 Create base directory structure for Kubernetes manifests in k8s/base/

## Phase 2: Foundational (Blocking Prerequisites)

- [x] T010 Install Minikube locally if not already installed
- [x] T011 Install kubectl CLI if not already installed
- [x] T012 Verify Minikube and kubectl compatibility with system resources
- [x] T013 Create Minikube start script with appropriate resource allocation in scripts/start-minikube.sh
- [x] T014 Start Minikube cluster with Docker driver and sufficient resources
- [x] T015 Verify Minikube cluster is operational with `minikube status` and `kubectl get nodes`
- [x] T016 Install Dapr in Kubernetes mode using `dapr init -k`
- [x] T017 Verify Dapr system pods are running with `kubectl get pods -n dapr-system`
- [x] T018 Create Dapr configuration for Kubernetes in k8s/dapr-config.yaml

## Phase 3: [US1] Kubernetes Manifest Creation

**Goal**: Create all necessary Kubernetes manifests for the application services

**Independent Test Criteria**:
- All Kubernetes manifests are syntactically correct
- All required services are defined in manifests
- Dapr annotations are properly configured

**Tasks**:

- [x] T020 [P] [US1] Create PostgreSQL deployment manifest in k8s/postgres-deployment.yaml
- [x] T021 [P] [US1] Create PostgreSQL service manifest in k8s/postgres-service.yaml
- [x] T022 [P] [US1] Create Redis deployment manifest in k8s/redis-deployment.yaml
- [x] T023 [P] [US1] Create Redis service manifest in k8s/redis-service.yaml
- [x] T024 [P] [US1] Create Zookeeper deployment manifest in k8s/zookeeper-deployment.yaml
- [x] T025 [P] [US1] Create Zookeeper service manifest in k8s/zookeeper-service.yaml
- [x] T026 [P] [US1] Create Kafka deployment manifest in k8s/kafka-deployment.yaml
- [x] T027 [P] [US1] Create Kafka service manifest in k8s/kafka-service.yaml
- [x] T028 [P] [US1] Create backend service deployment manifest with Dapr annotations in k8s/backend-deployment.yaml
- [x] T029 [P] [US1] Create backend service service manifest in k8s/backend-service.yaml
- [x] T030 [P] [US1] Create recurring consumer deployment manifest with Dapr annotations in k8s/recurring-consumer-deployment.yaml
- [x] T031 [P] [US1] Create frontend deployment manifest in k8s/frontend-deployment.yaml
- [x] T032 [P] [US1] Create frontend service manifest in k8s/frontend-service.yaml
- [x] T033 [US1] Create ConfigMap for application configuration in k8s/configmap.yaml
- [x] T034 [US1] Create PersistentVolumeClaim manifests for stateful services in k8s/pvc.yaml
- [ ] T035 [US1] Verify all manifests are syntactically correct with `kubectl apply --dry-run=client`

## Phase 4: [US2] Dapr Components for Kubernetes

**Goal**: Deploy Dapr components to the Kubernetes cluster

**Independent Test Criteria**:
- All Dapr components are registered in Kubernetes
- Components are properly configured for Kubernetes environment
- No component errors in Dapr operator logs

**Tasks**:

- [x] T040 [P] [US2] Convert pubsub component definition for Kubernetes in k8s/dapr-components/pubsub.yaml
- [x] T041 [P] [US2] Convert state store component definition for Kubernetes in k8s/dapr-components/statestore.yaml
- [x] T042 [P] [US2] Convert cron binding component definition for Kubernetes in k8s/dapr-components/cron-binding.yaml
- [x] T043 [P] [US2] Convert secrets component definition for Kubernetes in k8s/dapr-components/secrets.yaml
- [x] T044 [P] [US2] Create Kubernetes Secret for sensitive configuration in k8s/dapr-components/secret-store.yaml
- [ ] T045 [US2] Apply pub/sub component to Kubernetes cluster
- [ ] T046 [US2] Apply state store component to Kubernetes cluster
- [ ] T047 [US2] Apply cron binding component to Kubernetes cluster
- [ ] T048 [US2] Apply secrets component to Kubernetes cluster
- [ ] T049 [US2] Verify all Dapr components are registered with `kubectl get components.dapr.io`
- [ ] T050 [US2] Check Dapr operator logs for any component errors

## Phase 5: [US3] Container Image Preparation

**Goal**: Prepare and make container images available to Minikube

**Independent Test Criteria**:
- All application images are built successfully
- Images are available in Minikube's container environment
- Images can be pulled by Kubernetes without registry access

**Tasks**:

- [ ] T060 [P] [US3] Build backend service image with tag todo-app-backend:minikube
- [ ] T061 [P] [US3] Build frontend service image with tag todo-app-frontend:minikube
- [ ] T062 [P] [US3] Build recurring consumer image with tag todo-app-recurring-consumer:minikube
- [ ] T063 [US3] Load backend image into Minikube with `minikube image load`
- [ ] T064 [US3] Load frontend image into Minikube with `minikube image load`
- [ ] T065 [US3] Load recurring consumer image into Minikube with `minikube image load`
- [ ] T066 [US3] Verify images are available in Minikube with `minikube image ls`
- [ ] T067 [US3] Update deployment manifests to use the loaded images

## Phase 6: [US4] Application Deployment

**Goal**: Deploy all application services to the Minikube cluster

**Independent Test Criteria**:
- All application pods are running and ready
- Services are accessible within the cluster
- Dapr sidecars are properly injected and running

**Tasks**:

- [ ] T080 [US4] Apply namespace to cluster with `kubectl apply -f k8s/namespace.yaml`
- [ ] T081 [US4] Apply ConfigMap to cluster with `kubectl apply -f k8s/configmap.yaml`
- [ ] T082 [US4] Apply PVCs to cluster with `kubectl apply -f k8s/pvc.yaml`
- [ ] T083 [P] [US4] Apply PostgreSQL deployment and service to cluster
- [ ] T084 [P] [US4] Apply Redis deployment and service to cluster
- [ ] T085 [P] [US4] Apply Zookeeper deployment and service to cluster
- [ ] T086 [P] [US4] Apply Kafka deployment and service to cluster
- [ ] T087 [P] [US4] Apply backend deployment and service to cluster
- [ ] T088 [P] [US4] Apply recurring consumer deployment to cluster
- [ ] T089 [P] [US4] Apply frontend deployment and service to cluster
- [ ] T090 [US4] Wait for all pods to be in Running state
- [ ] T091 [US4] Verify Dapr sidecars are injected in application pods
- [ ] T092 [US4] Check application logs for any startup errors
- [ ] T093 [US4] Verify service-to-service communication within cluster

## Phase 7: [US5] Functional Verification

**Goal**: Verify the application functions correctly in the Kubernetes environment

**Independent Test Criteria**:
- Backend API endpoints return successful responses
- Dapr pub/sub messaging works correctly
- State store operations work via Dapr
- Cron bindings trigger as scheduled
- Service invocation works between services

**Tasks**:

- [ ] T100 [P] [US5] Test backend health endpoint via port-forward
- [ ] T101 [P] [US5] Test task creation via API and verify it's stored in state store
- [ ] T102 [P] [US5] Test task retrieval via API and verify it comes from state store
- [ ] T103 [P] [US5] Test task update via API and verify pub/sub event is published
- [ ] T104 [US5] Test Dapr pub/sub by publishing event and verifying subscription
- [ ] T105 [US5] Test Dapr state store by saving and retrieving task state
- [ ] T106 [US5] Test Dapr service invocation between backend services
- [ ] T107 [US5] Test Dapr secrets access for configuration
- [ ] T108 [US5] Verify cron binding triggers and processes reminders
- [ ] T109 [US5] Test recurring task processing functionality
- [ ] T110 [US5] Verify all functionality matches Docker Compose behavior

## Phase 8: Documentation & Readiness

**Goal**: Document the Minikube deployment and prepare for production considerations

**Independent Test Criteria**:
- Documentation is clear and accurate
- Known limitations are clearly communicated
- Deployment process is reproducible

**Tasks**:

- [x] T120 Update README with Minikube deployment instructions in README.md
- [x] T121 Create Minikube-specific troubleshooting guide in docs/minikube-troubleshooting.md
- [x] T122 Document differences between Docker Compose and Minikube deployments in docs/comparison.md
- [x] T123 Identify and document any limitations in docs/limitations.md
- [x] T124 Note areas for future improvement in docs/future-improvements.md
- [x] T125 Create checklist of items needed for production Kubernetes in docs/production-readiness.md
- [x] T126 Include considerations for production environments in docs/production-notes.md
- [x] T127 Note differences between local and cloud Kubernetes configurations in docs/local-vs-cloud.md