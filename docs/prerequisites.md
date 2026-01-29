# Prerequisites Installation Guide

This document outlines the tools and dependencies required to set up the development environment for the cloud infrastructure project.

## Required Tools

### 1. Docker Desktop
- **Download**: [Docker Desktop](https://www.docker.com/products/docker-desktop)
- **Minimum Version**: 4.0+
- **Platform Support**: Windows, macOS, Linux
- **Notes**: Ensure Kubernetes is enabled in Docker Desktop settings

### 2. kubectl
The Kubernetes command-line tool for interacting with clusters.

#### Installation Methods:
- **Windows**:
  ```powershell
  choco install kubernetes-cli
  ```
- **macOS**:
  ```bash
  brew install kubectl
  ```
- **Linux**:
  ```bash
  curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
  sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
  ```

#### Verification:
```bash
kubectl version --client
```

### 3. Minikube
A tool that runs a single-node Kubernetes cluster locally.

#### Installation Methods:
- **Windows**:
  ```powershell
  choco install minikube
  ```
- **macOS**:
  ```bash
  brew install minikube
  ```
- **Linux**:
  ```bash
  curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 \
  && chmod +x minikube \
  && sudo mv minikube /usr/local/bin
  ```

#### Verification:
```bash
minikube version
```

### 4. Dapr CLI
The command-line interface for Dapr (Distributed Application Runtime).

#### Installation Methods:
- **Windows**:
  ```powershell
  wget -q https://raw.githubusercontent.com/dapr/cli/master/install/install.ps1 -O install.ps1
  .\install.ps1
  ```
- **macOS/Linux**:
  ```bash
  wget -q https://raw.githubusercontent.com/dapr/cli/master/install/install.sh -O - | /bin/bash
  ```

#### Verification:
```bash
dapr --version
```

### 5. Git
Version control system.

#### Installation:
- **Windows/macOS**: Download from [git-scm.com](https://git-scm.com/downloads)
- **Linux**:
  ```bash
  # Ubuntu/Debian
  sudo apt update && sudo apt install git
  
  # CentOS/RHEL/Fedora
  sudo yum install git
  ```

#### Verification:
```bash
git --version
```

### 6. Azure CLI (for AKS)
Required for interacting with Azure services.

#### Installation:
- **Windows**:
  - Download from [Azure CLI installer](https://aka.ms/installazurecliwindows)
  - Or via Chocolatey: `choco install azure-cli`
- **macOS**:
  ```bash
  brew install azure-cli
  ```
- **Linux**:
  ```bash
  curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
  ```

#### Verification:
```bash
az --version
```

### 7. Terraform
Infrastructure as Code tool for defining cloud resources.

#### Installation:
- Download from [Terraform downloads](https://www.terraform.io/downloads)
- Or via package managers:
  - **Windows**: `choco install terraform`
  - **macOS**: `brew tap hashicorp/tap && brew install hashicorp/tap/terraform`
  - **Linux**:
    ```bash
    wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg
    echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
    sudo apt update && sudo apt install terraform
    ```

#### Verification:
```bash
terraform version
```

## Optional Tools

### 1. Visual Studio Code
Recommended IDE with extensions for:
- Kubernetes
- Docker
- Dapr
- Terraform

### 2. jq
Command-line JSON processor for working with API responses.

## Environment Setup

After installing all prerequisites, verify your setup by running the following commands:

```bash
# Check Docker
docker --version

# Check kubectl
kubectl version --client

# Check Minikube
minikube version

# Check Dapr
dapr --version

# Check Git
git --version

# Check Azure CLI (if installed)
az --version

# Check Terraform (if installed)
terraform version
```

## Troubleshooting

### Common Issues:

1. **Permission errors on Windows**: Run commands in an elevated PowerShell or Command Prompt
2. **kubectl not found**: Ensure kubectl is in your PATH
3. **Docker not running**: Start Docker Desktop before running other commands
4. **Minikube start fails**: Ensure virtualization is enabled in BIOS and no other hypervisors are running

### Resources:
- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/home/)
- [Dapr Documentation](https://docs.dapr.io/)
- [Azure CLI Documentation](https://docs.microsoft.com/en-us/cli/azure/)
- [Terraform Documentation](https://www.terraform.io/docs/index.html)