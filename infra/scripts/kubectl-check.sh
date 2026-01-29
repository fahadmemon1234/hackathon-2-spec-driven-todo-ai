#!/bin/bash
# Script to install kubectl and verify connectivity

echo "Checking kubectl installation and connectivity..."
echo "=================================================="

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo "kubectl is not installed. Installing kubectl..."

    # Detect OS
    OS="$(uname -s | tr '[:upper:]' '[:lower:]')"
    
    case "${OS}" in
        linux*)
            # Install kubectl on Linux
            curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
            chmod +x kubectl
            sudo mv kubectl /usr/local/bin/
            ;;
        darwin*)
            # Install kubectl on macOS
            if command -v brew &> /dev/null; then
                brew install kubectl
            else
                echo "Homebrew is required to install kubectl on macOS"
                exit 1
            fi
            ;;
        windows*)
            # Install kubectl on Windows (PowerShell)
            echo "Please install kubectl manually on Windows:"
            echo "Option 1: Using Chocolatey - choco install kubernetes-cli"
            echo "Option 2: Download from https://dl.k8s.io/release/v1.28.0/bin/windows/amd64/kubectl.exe"
            exit 1
            ;;
        *)
            echo "Unsupported OS: ${OS}"
            exit 1
            ;;
    esac
    
    echo "kubectl installed successfully"
else
    echo "kubectl is already installed: $(kubectl version --client --short)"
fi

# Verify kubectl connectivity
echo "Verifying kubectl connectivity..."
if kubectl cluster-info &> /dev/null; then
    echo "✅ Successfully connected to cluster"
    echo "Cluster Info:"
    kubectl cluster-info
    echo ""
    echo "Node Status:"
    kubectl get nodes
else
    echo "⚠️  Cannot connect to cluster. This is expected if Minikube is not running."
    echo "To start Minikube, run: minikube start"
    echo "Then verify connectivity again."
fi

echo ""
echo "kubectl check completed!"