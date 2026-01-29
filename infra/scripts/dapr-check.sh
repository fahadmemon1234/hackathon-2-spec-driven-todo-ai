#!/bin/bash
# Script to install Dapr CLI and verify installation

echo "Checking Dapr CLI installation and connectivity..."
echo "=================================================="

# Check if Dapr CLI is installed
if ! command -v dapr &> /dev/null; then
    echo "Dapr CLI is not installed. Installing Dapr CLI..."

    # Detect OS
    OS="$(uname -s | tr '[:upper:]' '[:lower:]')"
    
    case "${OS}" in
        linux*)
            # Install Dapr CLI on Linux
            wget -q https://raw.githubusercontent.com/dapr/cli/master/install/install.sh -O - | /bin/bash
            ;;
        darwin*)
            # Install Dapr CLI on macOS
            if command -v brew &> /dev/null; then
                brew install dapr/tap/dapr-cli
            else
                echo "Homebrew is required to install Dapr CLI on macOS"
                exit 1
            fi
            ;;
        windows*)
            # Install Dapr CLI on Windows (PowerShell)
            echo "Please install Dapr CLI manually on Windows:"
            echo "Option 1: Using Chocolatey - choco install dapr"
            echo "Option 2: Download from https://github.com/dapr/cli/releases"
            echo "Option 3: Using PowerShell -"
            echo "  mkdir -p \$HOME\\.dapr\\bin"
            echo "  Invoke-WebRequest -OutFile dapr.exe -Uri https://github.com/dapr/cli/releases/download/v1.11.0/dapr_windows_amd64.exe"
            echo "  Move-Item dapr.exe \$HOME\\.dapr\\bin"
            echo "  [Environment]::SetEnvironmentVariable('PATH', [Environment]::GetEnvironmentVariable('PATH', 'User') + \";\$HOME\\.dapr\\bin\")"
            exit 1
            ;;
        *)
            echo "Unsupported OS: ${OS}"
            exit 1
            ;;
    esac
    
    echo "Dapr CLI installed successfully"
else
    echo "Dapr CLI is already installed: $(dapr --version)"
fi

# Verify Dapr connectivity
echo "Verifying Dapr connectivity..."
if dapr status -k &> /dev/null; then
    echo "✅ Dapr is running in Kubernetes mode"
    echo "Dapr Status:"
    dapr status -k
else
    echo "⚠️  Dapr is not running in Kubernetes mode."
    echo "To initialize Dapr in Kubernetes mode, run: dapr init -k"
    echo "This requires a running Kubernetes cluster (e.g., Minikube)."
fi

echo ""
echo "Dapr CLI check completed!"