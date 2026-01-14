# Quickstart Guide: Local Kubernetes Deployment for Todo Chatbot Application

## Prerequisites

1. Install VirtualBox (7.0 or later)
2. Install Chocolatey package manager
3. Install Minikube, kubectl, and Helm:
   ```bash
   choco install minikube kubernetes-cli kubernetes-helm
   ```
4. Enable virtualization in BIOS (VT-x/AMD-V)
5. Ensure no other hypervisors are conflicting

## Setup and Deployment

### 1. Start Minikube Cluster
```bash
# Delete any existing clusters (optional)
minikube delete --all --purge

# Start new cluster with VirtualBox driver
minikube start --driver=virtualbox --cpus=2 --memory=4096 --disk-size=20000mb
```

### 2. Configure Docker Environment
```bash
# Point Docker CLI to Minikube's Docker daemon
minikube docker-env | Invoke-Expression
```

### 3. Build Docker Images
```bash
# Navigate to frontend directory and build image
cd frontend
docker build -t todo-frontend:local -f ../docker/frontend/Dockerfile .

# Navigate to backend directory and build image
cd ../backend
docker build -t todo-backend:local -f ../docker/backend/Dockerfile .
```

### 4. Verify Images
```bash
# Check that images are available in Minikube
minikube image ls | findstr todo-
```

### 5. Install Helm Chart
```bash
# Navigate to helm directory
cd ../helm

# Install the todo-app chart
helm install todo-app todo-app/ --values todo-app/values.yaml
```

### 6. Access the Application
```bash
# Get the frontend service URL
minikube service todo-frontend-service --url
```

## Verification Steps

1. Verify all pods are running:
   ```bash
   kubectl get pods
   ```

2. Verify services are available:
   ```bash
   kubectl get services
   ```

3. Access the frontend in your browser using the URL from step 6 above

4. Test all functionality:
   - Authentication
   - Task CRUD operations
   - Chatbot functionality

## Troubleshooting

- If Minikube fails to start, ensure VirtualBox is properly installed and virtualization is enabled in BIOS
- If images fail to build, ensure Docker is properly configured to use Minikube's daemon
- If services are not accessible, check that the correct ports are exposed and services are running
- If authentication fails, verify that the secrets are properly configured in the Kubernetes secret
- If the database connection fails, check that the DATABASE_URL is correctly set in the secret
- If the chatbot functionality doesn't work, verify that the OpenAI API key is properly configured