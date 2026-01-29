# Minikube Deployment Troubleshooting Guide

This document provides solutions to common issues encountered when deploying the Todo Application with Dapr integration to Minikube.

## Common Issues and Solutions

### 1. Minikube Cluster Not Starting

**Symptoms:**
- `minikube start` command fails
- Insufficient resources error
- Driver-related errors

**Solutions:**
1. Check system resources:
   ```bash
   # Ensure sufficient memory and CPU allocation
   minikube start --memory=6144mb --cpus=4
   ```

2. If using Docker driver, ensure Docker is running:
   ```bash
   # Verify Docker is running
   docker ps
   ```

3. Try with different driver if Docker fails:
   ```bash
   # For Windows
   minikube start --driver=hyperv
   
   # For macOS
   minikube start --driver=hyperkit
   ```

### 2. Dapr Not Installing in Kubernetes Mode

**Symptoms:**
- `dapr init -k` command fails
- Dapr system pods not running
- Error connecting to Kubernetes cluster

**Solutions:**
1. Verify kubectl is connected to Minikube:
   ```bash
   kubectl config current-context
   kubectl get nodes
   ```

2. Install Dapr CLI if not present:
   ```bash
   # Follow Dapr installation guide for your OS
   # Then try again:
   dapr init -k
   ```

3. Check Dapr system pods:
   ```bash
   kubectl get pods -n dapr-system
   kubectl logs -n dapr-system <pod-name>
   ```

### 3. Application Pods Failing to Start

**Symptoms:**
- Pods stuck in Pending or CrashLoopBackOff state
- Error logs mentioning Dapr sidecar issues
- Connection refused errors to Dapr services

**Solutions:**
1. Check if Dapr sidecar is properly injected:
   ```bash
   kubectl describe pod <pod-name> -n todo-app
   # Look for both application and daprd containers
   ```

2. Verify Dapr components are correctly configured:
   ```bash
   kubectl get components.dapr.io -n todo-app
   kubectl describe component <component-name> -n todo-app
   ```

3. Check for resource constraints:
   ```bash
   kubectl top nodes
   kubectl top pods -n todo-app
   ```

### 4. Kafka Connection Issues

**Symptoms:**
- Failed to connect to Kafka from application
- Pub/sub operations not working
- Error messages about broker connectivity

**Solutions:**
1. Verify Kafka pods are running:
   ```bash
   kubectl get pods -n todo-app | grep kafka
   ```

2. Check Kafka service:
   ```bash
   kubectl get svc kafka -n todo-app
   ```

3. Test connectivity from inside a pod:
   ```bash
   kubectl exec -it <backend-pod-name> -n todo-app -- nslookup kafka
   ```

### 5. Redis Connection Issues

**Symptoms:**
- Failed to connect to Redis from application
- State store operations not working
- Error messages about Redis connectivity

**Solutions:**
1. Verify Redis pods are running:
   ```bash
   kubectl get pods -n todo-app | grep redis
   ```

2. Check Redis service:
   ```bash
   kubectl get svc redis -n todo-app
   ```

3. Test connectivity from inside a pod:
   ```bash
   kubectl exec -it <backend-pod-name> -n todo-app -- nslookup redis
   ```

### 6. Service-to-Service Communication Issues

**Symptoms:**
- Applications can't communicate with each other
- Dapr service invocation not working
- Network timeouts between services

**Solutions:**
1. Verify service endpoints are accessible:
   ```bash
   kubectl get svc -n todo-app
   ```

2. Check if services are properly named and in the correct namespace:
   ```bash
   # Services should be accessible as <service-name>.<namespace>.svc.cluster.local
   kubectl exec -it <backend-pod-name> -n todo-app -- nslookup backend-service.todo-app.svc.cluster.local
   ```

3. Verify Dapr service invocation:
   ```bash
   # From inside a pod, test service invocation
   curl -X POST http://localhost:3500/v1.0/invoke/backend-service/method/health
   ```

### 7. Image Pull Issues

**Symptoms:**
- Pods stuck in ImagePullBackOff state
- Error pulling images from registry
- Image not found errors

**Solutions:**
1. Ensure images are loaded into Minikube:
   ```bash
   # Build and load images
   docker build -f Dockerfile.backend -t todo-app-backend:minikube .
   minikube image load todo-app-backend:minikube
   ```

2. Verify images are available in Minikube:
   ```bash
   minikube image ls | grep todo-app
   ```

3. Update deployment manifests to use correct image tags:
   ```bash
   # Make sure deployment files reference the correct image name and tag
   kubectl edit deployment backend-service -n todo-app
   ```

## Debugging Commands

### Check All Resources
```bash
kubectl get all -n todo-app
```

### Check Dapr Resources
```bash
kubectl get all -n dapr-system
kubectl get components.dapr.io -n todo-app
kubectl get configurations.dapr.io -n todo-app
```

### View Logs
```bash
# Application logs
kubectl logs -f deployment/backend-service -n todo-app

# Dapr sidecar logs
kubectl logs -f deployment/backend-service -n todo-app -c daprd

# Dapr operator logs
kubectl logs -f -n dapr-system deployment/dapr-operator
```

### Port Forwarding for Testing
```bash
# Access backend service
kubectl port-forward svc/backend-service 8000:8000 -n todo-app

# Access frontend service
kubectl port-forward svc/frontend 3000:3000 -n todo-app
```

## Resource Optimization

If experiencing resource constraints:

1. Reduce replica counts in deployments
2. Lower memory/CPU requests and limits
3. Use minikube's resource profile:
   ```bash
   minikube start --profile=minimal --memory=4096mb --cpus=2
   ```

## Verification Steps

After deployment, verify the system is working:

1. Check all pods are running:
   ```bash
   kubectl get pods -n todo-app
   ```

2. Verify Dapr sidecars are injected:
   ```bash
   kubectl get pods -n todo-app -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.containers[*].name}{"\n"}{end}'
   ```

3. Test application functionality:
   ```bash
   # Port forward to access the application
   kubectl port-forward svc/frontend 3000:3000 -n todo-app
   ```

4. Check Dapr health:
   ```bash
   dapr status -k
   ```