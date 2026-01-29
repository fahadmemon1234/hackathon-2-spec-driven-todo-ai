# Local Development Workflow with Dapr

This document provides a comprehensive guide for setting up and working with the local Dapr development environment.

## Overview

This setup allows you to develop and test Dapr-enabled services locally using Minikube as a Kubernetes cluster. The environment includes:

- Minikube: Single-node Kubernetes cluster
- Dapr: Distributed Application Runtime
- Sample service: Example application with Dapr sidecar
- Testing tools: Scripts to verify functionality

## Prerequisites

Before starting, ensure you have installed all required tools as outlined in the [prerequisites guide](../docs/prerequisites.md).

## Setting Up the Environment

### 1. Start Minikube

To start your local Kubernetes cluster with sufficient resources for Dapr:

```bash
# Navigate to the minikube directory
cd infra/minikube

# Start Minikube with the optimized configuration
./start.sh
```

### 2. Initialize Dapr

Once Minikube is running, initialize Dapr on the cluster:

```bash
# Navigate to the scripts directory
cd infra/scripts

# Initialize Dapr on Kubernetes
./dapr-init.sh
```

### 3. Deploy Sample Service

Deploy the sample service with Dapr sidecar:

```bash
# Navigate to the sample app directory
cd infra/sample-app

# Deploy the sample service
./deploy.sh
```

## Verifying the Setup

### 1. Check Dapr Dashboard

Verify that the Dapr dashboard is accessible:

```bash
# From the scripts directory
cd infra/scripts

# Verify dashboard accessibility
./verify-dashboard.sh
```

### 2. Test Service Invocation

Test that Dapr service invocation is working:

```bash
# From the tests directory
cd infra/tests

# Run service invocation test
./service-invocation-test.sh
```

## Working with Dapr Locally

### 1. Service Invocation

To invoke services using Dapr:

```bash
# Using Dapr CLI
dapr invoke --app-id sample-service --method healthz

# Using HTTP directly to Dapr sidecar
curl -X POST http://localhost:3500/v1.0/invoke/sample-service/method/healthz
```

### 2. State Management

To work with Dapr state stores:

```bash
# Using Dapr CLI
dapr state -k SET my-state-key '{"data":"value"}'
dapr state -k GET my-state-key
```

### 3. Pub/Sub Messaging

To work with Dapr pub/sub:

```bash
# Using Dapr CLI
dapr publish --pubsub pubsub --topic my-topic --data '{"message":"hello world"}'
```

## Development Workflow

### 1. Making Changes

1. Update your application code
2. Build a new Docker image:
   ```bash
   docker build -t your-app:latest .
   ```
3. Update your deployment YAML with the new image tag
4. Apply the updated deployment:
   ```bash
   kubectl apply -f your-deployment.yaml
   ```

### 2. Debugging

1. Check pod status:
   ```bash
   kubectl get pods
   ```
2. View logs:
   ```bash
   kubectl logs -l app=your-app
   kubectl logs -l app=your-app -c daprd  # Dapr sidecar logs
   ```
3. Describe pod for detailed information:
   ```bash
   kubectl describe pod -l app=your-app
   ```

### 3. Scaling

Scale your application as needed:

```bash
kubectl scale deployment your-app --replicas=3
```

## Useful Commands

### Kubernetes Commands
```bash
# View all pods
kubectl get pods

# View all services
kubectl get services

# View Dapr system pods
kubectl get pods -n dapr-system

# View logs for a specific pod
kubectl logs <pod-name>

# Port forward to access services locally
kubectl port-forward svc/your-service 8080:80
```

### Dapr Commands
```bash
# View Dapr status
dapr status -k

# Run an application with Dapr locally
dapr run --app-id my-app --app-port 3000 node app.js

# Access Dapr dashboard
dapr dashboard -k
```

## Troubleshooting

### Common Issues

1. **Minikube won't start**:
   - Ensure virtualization is enabled in BIOS
   - Check that no other hypervisors are running
   - Try running with admin privileges

2. **Dapr not initializing**:
   - Verify Kubernetes cluster is running
   - Check that kubectl can connect to the cluster
   - Ensure sufficient resources are allocated

3. **Pods stuck in Pending state**:
   - Check cluster resources: `kubectl top nodes`
   - Review pod events: `kubectl describe pod <pod-name>`
   - Verify Dapr system is running: `kubectl get pods -n dapr-system`

4. **Dapr sidecar not injected**:
   - Verify annotations in deployment YAML
   - Check Dapr operator is running: `kubectl get pods -n dapr-system`
   - Ensure `dapr.io/enabled: "true"` annotation is present

### Resource Optimization

- Adjust CPU and memory allocation in `infra/minikube/config.yaml` based on your system capabilities
- Monitor resource usage: `kubectl top nodes` and `kubectl top pods`
- Scale down unused deployments to conserve resources

## Cleaning Up

To stop your local development environment:

```bash
# Stop the sample service
kubectl delete -f infra/sample-app/deployment.yaml

# Uninstall Dapr
dapr uninstall -k

# Stop Minikube
minikube stop

# Optionally, delete the cluster to free up resources
minikube delete
```

## Next Steps

Once your local development environment is working properly:

1. Develop your actual application services
2. Configure Dapr components for your specific needs
3. Set up CI/CD pipelines for automated testing and deployment
4. Prepare for cloud deployment by creating infrastructure as code templates