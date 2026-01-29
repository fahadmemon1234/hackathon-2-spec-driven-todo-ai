#!/bin/bash
# Script to start Minikube cluster with sufficient resources for Dapr

echo "Starting Minikube cluster with resources for Dapr..."
echo "==================================================="

# Check if Minikube is already running
if minikube status &> /dev/null; then
    STATUS=$(minikube status --format="{{.Host}}" 2>/dev/null)
    if [ "$STATUS" = "Running" ]; then
        echo "✅ Minikube is already running"
        minikube status
        exit 0
    fi
fi

# Start Minikube with sufficient resources for Dapr
echo "Starting Minikube with 4 CPUs, 8GB memory, and 40GB disk..."
minikube start \
    --cpus=4 \
    --memory=8192mb \
    --disk-size=40gb \
    --driver=docker \
    --kubernetes-version=stable

if [ $? -eq 0 ]; then
    echo "✅ Minikube started successfully"
    
    # Set kubectl context to minikube
    kubectl config use-context minikube
    
    echo "Current cluster info:"
    kubectl cluster-info
    
    echo "Current node status:"
    kubectl get nodes
else
    echo "❌ Failed to start Minikube"
    exit 1
fi

echo ""
echo "Minikube cluster is ready for Dapr installation!"