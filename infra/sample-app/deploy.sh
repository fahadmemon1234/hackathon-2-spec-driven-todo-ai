#!/bin/bash
# Script to deploy sample service to local cluster

echo "Deploying sample service with Dapr sidecar to local cluster..."
echo "============================================================="

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl is not installed or not in PATH"
    exit 1
fi

# Check if a Kubernetes cluster is accessible
if ! kubectl cluster-info &> /dev/null; then
    echo "❌ Cannot connect to Kubernetes cluster"
    echo "Make sure Minikube is running: minikube start"
    exit 1
fi

# Check if Dapr is initialized
if ! kubectl get namespace dapr-system &> /dev/null; then
    echo "❌ Dapr is not installed in the Kubernetes cluster"
    echo "Please initialize Dapr first: dapr init -k"
    exit 1
fi

echo "Deploying sample service with Dapr sidecar..."

# Apply the deployment configuration
kubectl apply -f ./deployment.yaml

if [ $? -eq 0 ]; then
    echo "✅ Sample service deployment configuration applied successfully"
    
    # Wait for the pod to be ready
    echo "Waiting for sample service pod to be ready..."
    kubectl wait --for=condition=ready pod -l app=sample-service --timeout=180s
    
    if [ $? -eq 0 ]; then
        echo "✅ Sample service pod is ready"
        
        # Show the deployed resources
        echo "Sample Service Deployment:"
        kubectl get deployment sample-service
        
        echo "Sample Service Pod:"
        kubectl get pods -l app=sample-service
        
        echo "Sample Service Service:"
        kubectl get service sample-service
        
        # Show Dapr sidecar information
        echo "Dapr Sidecar Status:"
        kubectl describe pod -l app=sample-service | grep -A 15 "Containers:"
    else
        echo "⚠️  Sample service pod is not ready yet"
        echo "Sample Service Pod Status:"
        kubectl get pods -l app=sample-service
    fi
else
    echo "❌ Failed to deploy sample service"
    exit 1
fi

echo ""
echo "Sample service with Dapr sidecar deployed successfully!"