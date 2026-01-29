# Local Development Workflow

This document describes the local development workflow for the cloud infrastructure project using Minikube and Dapr.

## Prerequisites

Before starting local development, ensure you have installed all required tools as outlined in the [prerequisites guide](prerequisites.md).

## Setting Up the Local Environment

### 1. Starting Minikube

To start your local Kubernetes cluster:

```bash
# Start Minikube with sufficient resources for Dapr
minikube start --cpus=4 --memory=8192 --disk-size=40g

# Verify the cluster is running
kubectl cluster-info
```

### 2. Initializing Dapr

Once Minikube is running, initialize Dapr on the cluster:

```bash
# Initialize Dapr on Kubernetes
dapr init -k

# Verify Dapr is running
kubectl get pods -n dapr-system

# Check Dapr version
dapr --version
```

### 3. Deploying Services with Dapr Sidecars

To deploy a service with a Dapr sidecar, use annotations in your Kubernetes deployment:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-service
spec:
  replicas: 1
  selector:
    matchLabels:
      app: my-service
  template:
    metadata:
      labels:
        app: my-service
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "my-service"
        dapr.io/app-port: "8080"  # Port your app listens on
    spec:
      containers:
      - name: my-service
        image: my-service:latest
        ports:
        - containerPort: 8080
```

Apply the deployment:
```bash
kubectl apply -f my-service.yaml
```

## Working with Dapr

### 1. Accessing the Dapr Dashboard

To visualize your Dapr applications:

```bash
# Open the Dapr dashboard
dapr dashboard -k
```

This will open the dashboard in your default browser.

### 2. Service Invocation

To test service-to-service communication:

```bash
# Invoke a service using Dapr
dapr invoke --app-id target-service --method endpoint --data '{"message":"hello"}'
```

### 3. State Management

To interact with Dapr state stores:

```bash
# Save state
dapr state -k SET my-state-key '{"data":"value"}'

# Get state
dapr state -k GET my-state-key

# Delete state
dapr state -k DELETE my-state-key
```

### 4. Publishing and Subscribing to Events

To work with Dapr pub/sub:

```bash
# Publish a message to a topic
dapr publish --pubsub pubsub --topic my-topic --data '{"message":"hello world"}'
```

## Local Development Commands

### Useful Commands for Development

```bash
# View all pods
kubectl get pods

# View logs for a specific pod
kubectl logs -l app=my-service

# Port forward to access services locally
kubectl port-forward svc/my-service 8080:80

# Scale a deployment
kubectl scale deployment my-service --replicas=3

# Check Dapr sidecar injection
kubectl describe pod -l app=my-service
```

### Troubleshooting

1. **Pods stuck in Pending state**:
   ```bash
   kubectl get events --sort-by='.lastTimestamp'
   ```

2. **Dapr sidecar not injected**:
   - Verify the `dapr.io/enabled: "true"` annotation
   - Check that the Dapr operator is running: `kubectl get pods -n dapr-system`

3. **Service not accessible**:
   - Verify the service definition
   - Check if the pod is running and ready
   - Ensure the correct ports are exposed

## Development Cycle

### 1. Code, Build, Deploy Loop

1. Make changes to your application code
2. Build a new Docker image:
   ```bash
   docker build -t my-service:latest .
   ```
3. Update your deployment to use the new image
4. Apply the updated deployment:
   ```bash
   kubectl apply -f my-service.yaml
   ```
5. Verify the changes are working

### 2. Testing Locally

1. Test individual components using Dapr CLI:
   ```bash
   dapr run --app-id test-app --app-port 3000 node test-app.js
   ```
2. Test service invocation between components
3. Verify state management functionality
4. Test pub/sub messaging patterns

## Stopping the Environment

To stop your local development environment:

```bash
# Stop the Minikube cluster
minikube stop

# Optionally, delete the cluster to free up resources
minikube delete
```

## Tips for Efficient Development

1. **Use Minikube profiles**: Create different profiles for different projects
   ```bash
   minikube start -p project-a
   minikube start -p project-b
   ```

2. **Persistent volumes**: Use Minikube's persistent volume support for data that should survive restarts

3. **Resource optimization**: Adjust CPU and memory allocation based on your system capabilities

4. **Dapr configurations**: Use Dapr configurations to customize runtime behavior

5. **Logging and monitoring**: Set up proper logging to troubleshoot issues quickly

## Next Steps

Once your local development environment is set up and working:

1. Proceed to implement your application services
2. Configure Dapr components for your specific needs
3. Set up CI/CD pipelines for automated testing and deployment
4. Prepare for cloud deployment by creating infrastructure as code templates