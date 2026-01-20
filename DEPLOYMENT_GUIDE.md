# Advanced Cloud Deployment Guide

This guide provides instructions for deploying the Todo application with advanced features to various cloud platforms.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Local Deployment with Minikube](#local-deployment-with-minikube)
3. [Cloud Deployment](#cloud-deployment)
4. [Kafka and Dapr Configuration](#kafka-and-dapr-configuration)
5. [Monitoring and Logging](#monitoring-and-logging)
6. [CI/CD Pipeline](#cicd-pipeline)

## Prerequisites

Before deploying the application, ensure you have the following tools installed:

- Docker
- kubectl
- Helm
- Dapr CLI
- Cloud CLI tools (depending on your target platform)

### For Minikube:
- Minikube
- VirtualBox, Hyper-V, or Docker as VM driver

### For Cloud Platforms:
- Azure CLI (for AKS)
- Google Cloud SDK (for GKE)
- Oracle Cloud CLI (for OKE)

## Local Deployment with Minikube

### 1. Start Minikube
```bash
minikube start --driver=docker
```

### 2. Install Dapr
```bash
dapr init -k
```

### 3. Deploy Kafka using Strimzi
```bash
kubectl create namespace kafka
kubectl apply -f https://strimzi.io/install/latest?namespace=kafka
kubectl apply -f k8s/base/kafka-cluster.yaml
```

### 4. Deploy the application
```bash
kubectl apply -k k8s/minikube/
```

### 5. Access the application
```bash
minikube service frontend --url
```

## Cloud Deployment

### Azure Kubernetes Service (AKS)

#### 1. Create AKS cluster
```bash
az aks create \
  --resource-group myResourceGroup \
  --name myAKSCluster \
  --node-count 3 \
  --enable-addons monitoring \
  --generate-ssh-keys
```

#### 2. Connect to AKS
```bash
az aks get-credentials --resource-group myResourceGroup --name myAKSCluster
```

#### 3. Install Dapr
```bash
kubectl apply -f https://raw.githubusercontent.com/dapr/dapr/v1.12.0/releases/release-v1.12.0.yaml
```

#### 4. Deploy the application
```bash
kubectl apply -f aks/deployment.yaml
```

### Google Kubernetes Engine (GKE)

#### 1. Create GKE cluster
```bash
gcloud container clusters create my-cluster \
  --zone=us-central1-a \
  --num-nodes=3
```

#### 2. Get cluster credentials
```bash
gcloud container clusters get-credentials my-cluster --zone=us-central1-a
```

#### 3. Install Dapr
```bash
kubectl apply -f https://raw.githubusercontent.com/dapr/dapr/v1.12.0/releases/release-v1.12.0.yaml
```

#### 4. Deploy the application
```bash
kubectl apply -f gke/deployment.yaml
```

### Oracle Kubernetes Engine (OKE)

#### 1. Create OKE cluster
Follow Oracle Cloud documentation to create an OKE cluster.

#### 2. Get cluster credentials
```bash
oci ce cluster create-kubeconfig --cluster-id <cluster-id>
```

#### 3. Install Dapr
```bash
kubectl apply -f https://raw.githubusercontent.com/dapr/dapr/v1.12.0/releases/release-v1.12.0.yaml
```

#### 4. Deploy the application
```bash
kubectl apply -f oracle/deployment.yaml
```

## Kafka and Dapr Configuration

### Kafka Topics
The application uses the following Kafka topics:
- `task-events`: All task CRUD operations
- `reminders`: Scheduled reminder triggers
- `task-updates`: Real-time client sync

### Dapr Components
The application uses Dapr for:
- Pub/Sub: Kafka abstraction
- State Management: For application state
- Service Invocation: For inter-service communication
- Secrets Management: For secure credential storage

## Monitoring and Logging

### Prometheus and Grafana
The application includes monitoring configurations:

```bash
kubectl apply -f k8s/base/monitoring.yaml
```

### Application Metrics
Dapr provides built-in metrics for:
- Service invocation
- State management
- Pub/Sub operations
- Actor operations

## CI/CD Pipeline

The project includes a GitHub Actions workflow for continuous integration and deployment:

### Workflow Configuration
The workflow is defined in `.github/workflows/ci-cd.yml` and includes:
- Automated testing
- Docker image building
- Deployment to Minikube (development)
- Deployment to cloud platforms (production)

### Secrets Required
To use the CI/CD pipeline, configure the following secrets in your GitHub repository:

- `DOCKERHUB_USERNAME`: Your DockerHub username
- `DOCKERHUB_TOKEN`: Your DockerHub access token
- `AZURE_CREDENTIALS`: Azure service principal credentials (for AKS)
- `AZURE_RESOURCE_GROUP`: Azure resource group name
- `AZURE_CLUSTER_NAME`: AKS cluster name

## Advanced Features

### Recurring Tasks
Tasks can be configured to recur based on RRULE patterns. The recurring task service processes these events and creates new task instances.

### Due Dates and Reminders
Tasks with due dates trigger reminder events that are processed by the notification service.

### Real-time Sync
WebSocket connections enable real-time synchronization across all connected clients.

## Troubleshooting

### Common Issues
1. **Dapr sidecar not starting**: Ensure Dapr is properly installed in the cluster
2. **Kafka connectivity issues**: Verify Kafka cluster is running and accessible
3. **Database connection failures**: Check database credentials and network connectivity

### Debugging
Enable debug logging by setting the log level to "debug" in the deployment configurations.

## Scaling

### Horizontal Pod Autoscaling
The application includes HPA configurations for automatic scaling based on CPU and memory usage.

### Kafka Partitioning
Increase Kafka topic partitions to handle higher throughput.

## Security

### Network Policies
Implement network policies to restrict traffic between pods.

### RBAC
Configure Role-Based Access Control for secure access to Kubernetes resources.

### Secrets Management
Store sensitive information in Kubernetes secrets or external secret stores.

## Conclusion

This deployment guide provides instructions for deploying the Todo application with advanced features to various cloud platforms. The architecture leverages Kafka for event-driven communication and Dapr for simplified microservice development, providing scalability, reliability, and maintainability.