#!/bin/bash
# Local Development Environment Validation Script

echo "Validating local development environment..."
echo "=========================================="

# Check if Docker is running
echo "Checking Docker..."
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running or not installed"
    exit 1
else
    echo "✅ Docker is running"
fi

# Check if kubectl is installed
echo "Checking kubectl..."
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl is not installed"
    exit 1
else
    echo "✅ kubectl is installed: $(kubectl version --client --short)"
fi

# Check if minikube is installed
echo "Checking Minikube..."
if ! command -v minikube &> /dev/null; then
    echo "❌ Minikube is not installed"
    exit 1
else
    echo "✅ Minikube is installed: $(minikube version --short)"
fi

# Check if Dapr is installed
echo "Checking Dapr..."
if ! command -v dapr &> /dev/null; then
    echo "❌ Dapr is not installed"
    exit 1
else
    echo "✅ Dapr is installed: $(dapr --version)"
fi

# Check if git is installed
echo "Checking Git..."
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed"
    exit 1
else
    echo "✅ Git is installed: $(git --version)"
fi

# Check if Azure CLI is installed (optional)
echo "Checking Azure CLI..."
if command -v az &> /dev/null; then
    echo "✅ Azure CLI is installed: $(az version --output json | grep -o '\"azure-cli\": \"[^\"]*\"' | cut -d'"' -f4)"
else
    echo "⚠️  Azure CLI is not installed (this is optional for local development)"
fi

# Check if Terraform is installed (optional)
echo "Checking Terraform..."
if command -v terraform &> /dev/null; then
    echo "✅ Terraform is installed: $(terraform version | head -n1)"
else
    echo "⚠️  Terraform is not installed (this is optional for local development)"
fi

echo ""
echo "🎉 Local development environment validation completed!"
echo ""
echo "Summary:"
echo "- Essential tools: All installed and accessible"
echo "- Optional tools: Available for cloud deployment"
echo ""
echo "You're ready to proceed with the local development setup!"