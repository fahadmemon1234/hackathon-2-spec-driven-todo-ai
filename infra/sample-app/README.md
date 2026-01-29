# Sample Application with Dapr Integration

This directory contains a sample application that demonstrates Dapr integration in a Kubernetes environment.

## Components

### 1. Service Application
The sample service is a simple HTTP server that demonstrates Dapr capabilities:

- Service invocation
- State management
- Pub/Sub messaging

### 2. Dapr Configuration Files
- `deployment.yaml` - Kubernetes deployment with Dapr sidecar injection
- `statestore.yaml` - Dapr component for state management
- `pubsub.yaml` - Dapr component for pub/sub messaging

## Usage

To deploy the sample application to your Kubernetes cluster:

```bash
# Deploy the Dapr components
kubectl apply -f statestore.yaml
kubectl apply -f pubsub.yaml

# Deploy the application with Dapr sidecar
kubectl apply -f deployment.yaml

# Verify the deployment
kubectl get pods
kubectl get services
```

## Application Endpoints

Once deployed, the sample application provides the following endpoints:

- `GET /health` - Health check endpoint
- `POST /invoke` - Service invocation demonstration
- `POST /state` - State management demonstration
- `POST /publish` - Pub/Sub messaging demonstration

## Dapr Integration

The application demonstrates the following Dapr capabilities:

1. **Service Invocation**: Call other services using Dapr's service discovery
2. **State Management**: Store and retrieve state using Dapr's state API
3. **Pub/Sub**: Send and receive messages using Dapr's pub/sub API
4. **Secrets Management**: Access secrets securely through Dapr