#!/bin/bash
# Script to initialize Dapr on local Kubernetes cluster

echo "Initializing Dapr on local Kubernetes cluster..."
echo "==============================================="

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

# Check if Dapr CLI is available
if ! command -v dapr &> /dev/null; then
    echo "❌ Dapr CLI is not installed or not in PATH"
    echo "Please install Dapr CLI first"
    exit 1
fi

# Check if Dapr is already initialized in Kubernetes
if kubectl get namespace dapr-system &> /dev/null; then
    echo "⚠️  Dapr is already installed in Kubernetes"
    echo "Dapr Status:"
    dapr status -k
    echo ""
    echo "If you need to reinstall, run: dapr uninstall -k"
    exit 0
fi

echo "Installing Dapr on Kubernetes cluster..."

# Initialize Dapr in Kubernetes mode
dapr init -k

if [ $? -eq 0 ]; then
    echo "✅ Dapr initialized successfully in Kubernetes mode"
    
    # Wait for Dapr system pods to be ready
    echo "Waiting for Dapr system pods to be ready..."
    kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=dapr --timeout=180s -n dapr-system
    
    if [ $? -eq 0 ]; then
        echo "✅ All Dapr system pods are ready"
        
        # Show Dapr status
        echo "Dapr Status:"
        dapr status -k
        
        # Show Dapr system pods
        echo "Dapr System Pods:"
        kubectl get pods -n dapr-system
    else
        echo "⚠️  Some Dapr system pods are not ready yet"
        echo "Dapr System Pods Status:"
        kubectl get pods -n dapr-system
    fi
else
    echo "❌ Failed to initialize Dapr in Kubernetes mode"
    exit 1
fi

echo ""
echo "Dapr is ready to use with your applications!"