# Local Deployment – Minikube Implementation Plan

## Technical Context

**Project**: Todo Application – Dapr Integration (Local Docker Compose)
**Component**: Local Deployment using Minikube (Kubernetes)
**Status**: Optional / Planned

**Current Environment**:
- Application running on Docker Compose with Dapr integration
- Backend service with Dapr sidecar
- Kafka, Redis, PostgreSQL services
- All Dapr components (pub/sub, state store, cron, secrets, service invocation) implemented

**Target Environment**:
- Minikube (single-node Kubernetes cluster)
- Kubernetes-native deployment
- Dapr in Kubernetes mode
- Containerized application services

**Unknowns**:
- Minikube installation status on target machine
- Kubernetes version compatibility with current Dapr version
- Resource requirements for Minikube cluster
- Network configuration for external access

## Constitution Check

Following the project constitution principles:
- Maintain backward compatibility where possible
- Ensure secure handling of secrets
- Implement proper error handling and logging
- Follow clean code practices
- Maintain performance standards
- Ensure proper testing coverage

## Implementation Plan

### PHASE 1: PREPARATION & ENVIRONMENT SETUP

**Task MK-01**: Install and validate Minikube environment
- Description: Install and validate Minikube and kubectl on the local machine
- Inputs: Docker Desktop installed, Application running on Docker Compose
- Actions:
  - Download and install Minikube
  - Download and install kubectl CLI
  - Verify Minikube and kubectl installations and versions
- Output: Minikube and kubectl CLIs available and properly configured
- Verification: 
  - `minikube version` returns version info
  - `kubectl version` returns client/server versions
  - `kubectl config current-context` shows active context

### PHASE 2: MINIKUBE CLUSTER INITIALIZATION

**Task MK-02**: Start local Kubernetes cluster
- Description: Initialize and start a single-node Kubernetes cluster using Minikube
- Inputs: Minikube installed, Docker runtime available
- Actions:
  - Start Minikube cluster with Docker driver
  - Configure cluster resources (CPU, memory)
  - Verify cluster is operational
- Output: Single-node Kubernetes cluster running locally
- Verification:
  - `minikube status` shows running cluster
  - `kubectl get nodes` shows active node

### PHASE 3: DAPR INSTALLATION ON MINIKUBE

**Task MK-03**: Install Dapr control plane in Kubernetes
- Description: Deploy Dapr runtime to the Minikube cluster in Kubernetes mode
- Inputs: Running Minikube cluster
- Actions:
  - Use `dapr init -k` to install Dapr in Kubernetes mode
  - Verify Dapr system pods are running
  - Check Dapr placement, operator, and sidecar injector services
- Output: Dapr control plane installed in Kubernetes cluster
- Verification:
  - `kubectl get pods -n dapr-system` shows all Dapr pods running
  - Dapr placement, operator, and sidecar injector pods are operational

### PHASE 4: APPLICATION IMAGE PREPARATION

**Task MK-04**: Prepare container images for Kubernetes
- Description: Make application container images available to the Minikube cluster
- Inputs: Existing backend and consumer Dockerfiles
- Actions:
  - Build application images using existing Dockerfiles
  - Load images into Minikube's Docker environment using `minikube image load`
  - Verify images are available in Minikube
- Output: Application container images available in Minikube
- Verification:
  - `minikube image ls` shows application images
  - Kubernetes can pull images without registry access

### PHASE 5: KUBERNETES MANIFEST CREATION

**Task MK-05**: Create Kubernetes manifests for application
- Description: Define Kubernetes resources for all application services
- Inputs: Application services definition (backend, consumer, Kafka, Redis, PostgreSQL)
- Actions:
  - Create Deployment manifests for backend service
  - Create Deployment manifests for recurring consumer service
  - Create Deployment manifests for supporting services (Kafka, Redis, PostgreSQL, Zookeeper)
  - Create Service manifests for internal service communication
  - Create ConfigMaps for configuration values
  - Create PersistentVolumeClaims for stateful services
- Output: Complete Kubernetes YAML manifests for the application
- Verification:
  - `kubectl apply --dry-run=client -f manifests/` shows no syntax errors
  - All required resources are defined

### PHASE 6: DAPR SIDECAR INJECTION

**Task MK-06**: Enable Dapr sidecars for services
- Description: Configure Kubernetes deployments to inject Dapr sidecars
- Inputs: Kubernetes deployments created
- Actions:
  - Add Dapr annotations to pod specs:
    - `dapr.io/enabled: "true"`
    - `dapr.io/app-id: "backend-service"`
    - `dapr.io/app-port: "8000"`
    - `dapr.io/config: "dapr-config"`
  - Apply updated manifests with sidecar injection
- Output: Dapr sidecars automatically injected into application pods
- Verification:
  - `kubectl get pods` shows 2 containers per application pod (app + dapr)
  - `kubectl describe pod <pod-name>` shows both containers

### PHASE 7: DAPR COMPONENT DEPLOYMENT

**Task MK-07**: Deploy Dapr components to cluster
- Description: Apply Dapr component definitions to the Kubernetes cluster
- Inputs: Existing Dapr component definitions (pubsub.yaml, statestore.yaml, etc.)
- Actions:
  - Convert component files to Kubernetes secrets/configmaps if needed
  - Apply pub/sub (Kafka) component to cluster
  - Apply state store (Redis) component to cluster
  - Apply cron binding component to cluster
  - Apply secret store component to cluster
- Output: Dapr components registered and operational in Kubernetes
- Verification:
  - `kubectl get components.dapr.io` shows all components
  - No component errors in Dapr operator logs

### PHASE 8: APPLICATION DEPLOYMENT & STARTUP

**Task MK-08**: Deploy application services to Minikube
- Description: Deploy all application services to the Minikube cluster
- Inputs: Kubernetes manifests, Dapr components applied
- Actions:
  - Apply all Kubernetes manifests to the cluster
  - Monitor pod startup and readiness
  - Verify service-to-service communication
- Output: All application pods running and communicating
- Verification:
  - `kubectl get pods` shows all pods in Running state
  - `kubectl describe pod <pod-name>` shows no crash loops or errors

### PHASE 9: FUNCTIONAL VERIFICATION

**Task MK-09**: Verify application behavior in Minikube
- Description: Test that the application functions correctly in the Kubernetes environment
- Inputs: Running application pods in Minikube
- Actions:
  - Access backend service via port-forward
  - Test Dapr pub/sub messaging functionality
  - Verify state store read/write operations
  - Verify cron binding triggers and recurring task processing
  - Test service invocation between components
- Output: Application behaves identically to Docker Compose setup
- Verification:
  - Successful HTTP responses from backend API
  - Kafka events processed via Dapr pub/sub
  - State updates persisted via Dapr state store
  - Cron triggers execute as scheduled
  - Service invocations work correctly

### PHASE 10: DOCUMENTATION & STATUS UPDATE

**Task MK-10**: Document Minikube deployment outcome
- Description: Record the results of the Minikube deployment and update project documentation
- Inputs: Successful or failed deployment attempt
- Actions:
  - Document verification results
  - Update deployment status (Optional or Complete)
  - Note any limitations or configuration differences
  - Create troubleshooting guide for Minikube deployment
- Output: Updated project documentation with Minikube deployment information
- Verification:
  - sp.plan execution notes saved
  - Status updated in project tracking
  - Documentation is clear and actionable

## Gates Evaluation

### Gate 1: Environment Compatibility
- **Check**: Is Minikube compatible with current system resources?
- **Status**: NEEDS VERIFICATION
- **Action**: Assess available RAM, CPU, and disk space before proceeding

### Gate 2: Kubernetes Version Compatibility
- **Check**: Does the current Dapr version support the Minikube Kubernetes version?
- **Status**: NEEDS VERIFICATION
- **Action**: Check Dapr compatibility matrix before installation

### Gate 3: Resource Requirements
- **Check**: Does the local machine have sufficient resources for Minikube cluster?
- **Status**: NEEDS VERIFICATION
- **Action**: Plan resource allocation (recommended 4GB+ RAM, 2+ CPUs)

## Research Required

Before proceeding with implementation, the following research is needed:

1. **Minikube Resource Requirements**: Determine minimum and recommended resources for running the full application stack
2. **Dapr Kubernetes Best Practices**: Research optimal Dapr configuration for Kubernetes deployment
3. **Image Management Strategy**: Determine best approach for managing container images in Minikube
4. **Service Exposure Options**: Research options for exposing services externally from Minikube
5. **Persistent Storage Options**: Investigate storage solutions for stateful services in Minikube

## Data Model Considerations

The existing data model remains unchanged for the Kubernetes deployment. All entities (Task, Reminder, RecurrenceMetadata) and their relationships will be preserved.

## Contract Considerations

All existing API contracts remain unchanged. The Kubernetes deployment is an infrastructure change that doesn't affect the application's external interfaces.

## Quickstart Guide

For developers wanting to run the application on Minikube:

1. Install Minikube and kubectl
2. Start Minikube cluster
3. Install Dapr in Kubernetes mode
4. Build and load application images
5. Apply Kubernetes manifests
6. Verify functionality via port-forward