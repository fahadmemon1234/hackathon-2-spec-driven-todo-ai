# Quickstart Guide for Minikube Deployment

## Prerequisites

- Docker Desktop installed and running
- Minikube installed (version 1.20 or higher recommended)
- kubectl installed (compatible with Minikube version)
- At least 6GB of RAM and 4 CPU cores available
- Administrative privileges for running Docker and Minikube

## Setup Instructions

### 1. Start Minikube Cluster

```bash
# Start Minikube with sufficient resources for the application
minikube start --memory=6144 --cpus=4 --disk-size=10g

# Verify cluster is running
kubectl get nodes
```

### 2. Install Dapr in Kubernetes Mode

```bash
# Install Dapr control plane in the cluster
dapr init -k

# Verify Dapr is running
kubectl get pods -n dapr-system
```

### 3. Build and Load Application Images

```bash
# Build the application images
docker build -f Dockerfile.backend -t todo-app-backend:latest .
docker build -f Dockerfile.frontend -t todo-app-frontend:latest .

# Load images into Minikube
minikube image load todo-app-backend:latest
minikube image load todo-app-frontend:latest

# Verify images are loaded
minikube image ls | grep todo-app
```

### 4. Deploy Supporting Services

```bash
# Create namespace for the application
kubectl create namespace todo-app

# Deploy PostgreSQL
kubectl apply -f k8s/postgres-deployment.yaml
kubectl apply -f k8s/postgres-service.yaml

# Deploy Redis
kubectl apply -f k8s/redis-deployment.yaml
kubectl apply -f k8s/redis-service.yaml

# Deploy Kafka and Zookeeper
kubectl apply -f k8s/zookeeper-deployment.yaml
kubectl apply -f k8s/zookeeper-service.yaml
kubectl apply -f k8s/kafka-deployment.yaml
kubectl apply -f k8s/kafka-service.yaml

# Wait for all services to be ready
kubectl wait --for=condition=ready pod -l app=postgres --timeout=300s
kubectl wait --for=condition=ready pod -l app=redis --timeout=300s
kubectl wait --for=condition=ready pod -l app=kafka --timeout=300s
```

### 5. Deploy Dapr Components

```bash
# Apply Dapr component definitions
kubectl apply -f components/pubsub.yaml
kubectl apply -f components/statestore.yaml
kubectl apply -f components/secrets.yaml
kubectl apply -f components/cron-binding.yaml

# Verify components are registered
kubectl get components.dapr.io
```

### 6. Deploy Application Services

```bash
# Deploy backend service with Dapr sidecar
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/backend-service.yaml

# Deploy frontend service
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/frontend-service.yaml

# Deploy recurring consumer
kubectl apply -f k8s/recurring-consumer-deployment.yaml

# Wait for application pods to be ready
kubectl wait --for=condition=ready pod -l app=backend --timeout=300s
kubectl wait --for=condition=ready pod -l app=frontend --timeout=300s
```

### 7. Access the Application

```bash
# Port forward to access the backend service
kubectl port-forward svc/backend-service 8000:8000 -n todo-app

# In another terminal, port forward to access the frontend
kubectl port-forward svc/frontend-service 3001:3000 -n todo-app

# Access the application at http://localhost:3001
```

## Common Commands

```bash
# Check all pods
kubectl get pods -n todo-app

# Check Dapr sidecar logs
kubectl logs <pod-name> -c daprd -n todo-app

# Check application logs
kubectl logs <pod-name> -n todo-app

# Scale backend service
kubectl scale deployment backend-service --replicas=2 -n todo-app

# Check services
kubectl get svc -n todo-app

# Check Dapr components
kubectl get components.dapr.io -n todo-app

# Check Dapr subscriptions
kubectl get subscriptions.dapr.io -n todo-app
```

## Troubleshooting

1. **Pods stuck in Pending state**:
   - Check if Minikube has sufficient resources
   - Verify Dapr control plane is running: `kubectl get pods -n dapr-system`

2. **Dapr sidecar not injected**:
   - Verify Dapr annotations are present in deployment
   - Check if Dapr operator is running: `kubectl get pods -n dapr-system`

3. **Service-to-service communication fails**:
   - Verify service names and namespaces
   - Check if Dapr sidecars are properly configured

4. **Image pull errors**:
   - Ensure images are loaded into Minikube: `minikube image load <image-name>`
   - Verify image names match those in deployment manifests

## Stopping the Application

```bash
# Stop port forwards with Ctrl+C

# Delete application deployments
kubectl delete -f k8s/backend-deployment.yaml
kubectl delete -f k8s/frontend-deployment.yaml
kubectl delete -f k8s/recurring-consumer-deployment.yaml

# Delete supporting services
kubectl delete -f k8s/postgres-deployment.yaml
kubectl delete -f k8s/redis-deployment.yaml
kubectl delete -f k8s/kafka-deployment.yaml

# Stop Minikube
minikube stop
```