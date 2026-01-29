# Quickstart Guide: Cloud & Infrastructure Setup

**Feature**: 19-cloud-infrastructure-specification
**Created**: 2026-01-28
**Status**: Complete
**Author**: Qwen AI

## Overview

This quickstart guide provides step-by-step instructions to set up the cloud infrastructure for the todo application, starting with local development using Minikube and Dapr, then progressing toward cloud deployment.

## Prerequisites

Before starting, ensure you have the following tools installed:

- Docker Desktop (with Kubernetes enabled) or a Kubernetes cluster
- kubectl (Kubernetes command-line tool)
- Minikube (for local development)
- Dapr CLI
- Git
- A cloud provider account (Azure, Google Cloud, or Oracle Cloud) for cloud deployment

## Phase 1: Local Development Setup

### Step 1: Install Prerequisites

1. Install Docker Desktop from [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
2. Install kubectl:
   - On macOS: `brew install kubectl`
   - On Windows: `choco install kubernetes-cli`
   - On Linux: `curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"`
3. Install Minikube:
   - Visit [https://minikube.sigs.k8s.io/docs/start/](https://minikube.sigs.k8s.io/docs/start/) for installation instructions
4. Install Dapr CLI:
   - On macOS/Linux: `wget -q https://raw.githubusercontent.com/dapr/cli/master/install/install.sh -O - | /bin/bash`
   - On Windows: Download from [https://github.com/dapr/cli/releases](https://github.com/dapr/cli/releases)

### Step 2: Start Minikube Cluster

1. Start Minikube with sufficient resources:
   ```bash
   minikube start --cpus=4 --memory=8192
   ```

2. Verify the cluster is running:
   ```bash
   kubectl cluster-info
   ```

### Step 3: Install Dapr on Minikube

1. Initialize Dapr on your Kubernetes cluster:
   ```bash
   dapr init -k
   ```

2. Verify Dapr is running:
   ```bash
   kubectl get pods -n dapr-system
   ```

3. Check Dapr version:
   ```bash
   dapr --version
   ```

### Step 4: Deploy Sample Service with Dapr Sidecar

1. Create a simple service configuration file (`sample-service.yaml`):
   ```yaml
   apiVersion: v1
   kind: Service
   metadata:
     name: sample-service
     labels:
       app: sample-service
   spec:
     selector:
       app: sample-service
     ports:
       - protocol: TCP
         port: 80
         targetPort: 3000
     type: LoadBalancer
   ---
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: sample-service
     labels:
       app: sample-service
   spec:
     replicas: 1
     selector:
       matchLabels:
         app: sample-service
     template:
       metadata:
         labels:
           app: sample-service
         annotations:
           dapr.io/enabled: "true"
           dapr.io/app-id: "sample-service"
           dapr.io/app-port: "3000"
       spec:
         containers:
         - name: sample-service
           image: nginx:latest
           ports:
           - containerPort: 3000
   ```

2. Apply the configuration:
   ```bash
   kubectl apply -f sample-service.yaml
   ```

3. Wait for the pod to be ready:
   ```bash
   kubectl get pods --watch
   ```

### Step 5: Verify Dapr Functionality

1. Check that the Dapr sidecar is injected:
   ```bash
   kubectl describe pod -l app=sample-service
   ```
   Look for two containers in the pod: the application container and the daprd container.

2. Access the Dapr dashboard:
   ```bash
   dapr dashboard -k
   ```
   This will open the Dapr dashboard in your browser.

3. Test service invocation:
   ```bash
   dapr invoke --app-id sample-service --method healthz
   ```

## Phase 2: Kafka Integration (Local)

### Step 1: Set Up Kafka Locally

1. If you don't already have a Kafka setup, create a `kafka-local.yaml`:
   ```yaml
   version: '3.8'
   
   services:
     zookeeper:
       image: confluentinc/cp-zookeeper:latest
       environment:
         ZOOKEEPER_CLIENT_PORT: 2181
         ZOOKEEPER_TICK_TIME: 2000
   
     kafka:
       image: confluentinc/cp-kafka:latest
       depends_on:
         - zookeeper
       ports:
         - "9092:9092"
       environment:
         KAFKA_BROKER_ID: 1
         KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
         KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
         KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
   ```

2. Start Kafka:
   ```bash
   docker-compose -f kafka-local.yaml up -d
   ```

### Step 2: Connect Services to Kafka

1. Create a Dapr component for Kafka (`kafka-component.yaml`):
   ```yaml
   apiVersion: dapr.io/v1alpha1
   kind: Component
   metadata:
     name: pubsub
     namespace: default
   spec:
     type: pubsub.kafka
     version: v1
     metadata:
     - name: brokers
       value: "localhost:9092"  # Adjust if using different host/port
     - name: consumerGroup
       value: "myGroup"
     - name: clientID
       value: "myClientID"
     - name: authRequired
       value: "false"
   ```

2. Apply the Kafka component:
   ```bash
   kubectl apply -f kafka-component.yaml
   ```

### Step 3: Test Event Flow

1. Publish a test message using Dapr:
   ```bash
   dapr publish --pubsub pubsub --topic test-topic --data '{"message": "Hello, Kafka!"}'
   ```

2. Verify the message was published by checking Dapr logs:
   ```bash
   kubectl logs -l app=sample-service -c daprd
   ```

## Phase 3: CI/CD Foundation

### Step 1: Create GitHub Actions Workflow

1. Create the workflow directory:
   ```bash
   mkdir -p .github/workflows
   ```

2. Create a basic CI workflow file (`.github/workflows/ci-main.yaml`):
   ```yaml
   name: CI Pipeline

   on:
     push:
       branches: [ main, develop ]
     pull_request:
       branches: [ main ]

   jobs:
     build-and-test:
       runs-on: ubuntu-latest

       steps:
       - uses: actions/checkout@v3

       - name: Set up Python
         uses: actions/setup-python@v4
         with:
           python-version: '3.13'

       - name: Install dependencies
         run: |
           python -m pip install --upgrade pip
           pip install -r requirements.txt

       - name: Run tests
         run: |
           python -m pytest tests/

       - name: Build Docker image
         run: |
           docker build -t todo-app:${{ github.sha }} .
       
       - name: Run security scan
         run: |
           # Add security scanning here
           echo "Running security scan..."

       - name: Report status
         if: always()
         run: |
           echo "Build completed at $(date)"
   ```

### Step 2: Add Build Status Badge to README

1. Add the following badge to your README.md:
   ```markdown
   ![CI Pipeline](https://github.com/your-username/your-repo/actions/workflows/ci-main.yaml/badge.svg)
   ```

## Phase 4: Monitoring Setup (Local)

### Step 1: Install Prometheus in Minikube

1. Create a Prometheus configuration (`prometheus-config.yaml`):
   ```yaml
   apiVersion: v1
   kind: ConfigMap
   metadata:
     name: prometheus-server-conf
     labels:
       name: prometheus-server-conf
   data:
     prometheus.rules: |-
       {}
     prometheus.yml: |-
       global:
         scrape_interval: 5s
         evaluation_interval: 5s
       rule_files:
         - /etc/prometheus/prometheus.rules
       scrape_configs:
         - job_name: 'kubernetes-apiservers'
           kubernetes_sd_configs:
           - role: endpoints
           scheme: https
           tls_config:
             ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
           bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
           relabel_configs:
           - source_labels: [__meta_kubernetes_namespace, __meta_kubernetes_service_name, __meta_kubernetes_endpoint_port_name]
             action: keep
             regex: default;kubernetes;https
         
         - job_name: 'kubernetes-nodes'
           kubernetes_sd_configs:
           - role: node
           scheme: https
           tls_config:
             ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
           bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
           relabel_configs:
           - action: labelmap
             regex: __meta_kubernetes_node_label_(.+)
           - target_label: __address__
             replacement: kubernetes.default.svc:443
           - source_labels: [__meta_kubernetes_node_name]
             regex: (.+)
             target_label: __metrics_path__
             replacement: /api/v1/nodes/${1}/proxy/metrics
       
         - job_name: 'kubernetes-pods'
           kubernetes_sd_configs:
           - role: pod
           relabel_configs:
           - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
             action: keep
             regex: true
           - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
             action: replace
             target_label: __metrics_path__
             regex: (.+)
           - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
             action: replace
             regex: ([^:]+)(?::\d+)?;(\d+)
             replacement: $1:$2
             target_label: __address__
           - action: labelmap
             regex: __meta_kubernetes_pod_label_(.+)
           - source_labels: [__meta_kubernetes_namespace]
             action: replace
             target_label: kubernetes_namespace
           - source_labels: [__meta_kubernetes_pod_name]
             action: replace
             target_label: kubernetes_pod_name
   ```

2. Create a Prometheus deployment (`prometheus-deployment.yaml`):
   ```yaml
   apiVersion: v1
   kind: Service
   metadata:
     name: prometheus-service
     annotations:
       prometheus.io/scrape: 'true'
       prometheus.io/port:   '9090'
   spec:
     selector:
       app: prometheus-server
     type: NodePort  
     ports:
       - port: 9090
         targetPort: 9090
         nodePort: 30090
   ---
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: prometheus-deployment
   spec:
     replicas: 1
     selector:
       matchLabels:
         app: prometheus-server
     template:
       metadata:
         labels:
           app: prometheus-server
       spec:
         containers:
           - name: prometheus
             image: prom/prometheus:latest
             args:
               - '--storage.tsdb.retention.time=200h'
               - '--config.file=/etc/prometheus/prometheus.yml'
               - '--storage.tsdb.path=/prometheus/'
               - '--web.console.libraries=/etc/prometheus/console_libraries'
               - '--web.console.templates=/etc/prometheus/consoles'
               - '--web.enable-lifecycle'
             ports:
               - containerPort: 9090
             resources:
               requests:
                 cpu: 100m
                 memory: 100Mi
               limits:
                 cpu: 500m
                 memory: 500Mi
             volumeMounts:
               - name: prometheus-config-volume
                 mountPath: /etc/prometheus/
               - name: prometheus-storage-volume
                 mountPath: /prometheus/
         volumes:
           - name: prometheus-config-volume
             configMap:
               defaultMode: 420
               name: prometheus-server-conf
           - name: prometheus-storage-volume
             emptyDir: {}
   ```

3. Deploy Prometheus:
   ```bash
   kubectl apply -f prometheus-config.yaml
   kubectl apply -f prometheus-deployment.yaml
   ```

### Step 2: Access Prometheus Dashboard

1. Expose Prometheus service:
   ```bash
   minikube service prometheus-service
   ```

2. This will provide a URL to access the Prometheus dashboard.

## Phase 5: Cloud Preparation

### Step 1: Choose Cloud Provider

Based on our research, we recommend starting with Azure AKS due to its strong Dapr integration and documentation. However, you can choose based on your specific requirements:

- **Azure AKS**: Strong Dapr support, good documentation, free tier available
- **Google GKE**: Reliable Kubernetes service, good for multi-cloud strategies
- **Oracle OKE**: Cost-effective option, especially for existing Oracle customers

### Step 2: Prepare Cloud Account

1. Sign up for your chosen cloud provider account
2. Install the cloud CLI tool:
   - Azure: `az` - Install Azure CLI
   - Google: `gcloud` - Install Google Cloud SDK
   - Oracle: `oci` - Install Oracle Cloud Infrastructure CLI
3. Authenticate with your account:
   - Azure: `az login`
   - Google: `gcloud auth login`
   - Oracle: `oci setup config`

### Step 3: Prepare Infrastructure as Code

1. Create a directory for infrastructure code:
   ```bash
   mkdir -p infrastructure/aks  # or gke, oke
   ```

2. Create a basic cluster definition template (for Azure):
   ```hcl
   # infrastructure/aks/main.tf
   terraform {
     required_providers {
       azurerm = {
         source  = "hashicorp/azurerm"
         version = "~> 3.0"
       }
     }
   }

   provider "azurerm" {
     features {}
   }

   resource "azurerm_resource_group" "aks_rg" {
     name     = "todo-app-rg"
     location = var.location
   }

   resource "azurerm_kubernetes_cluster" "aks_cluster" {
     name                = "todo-aks-cluster"
     location            = azurerm_resource_group.aks_rg.location
     resource_group_name = azurerm_resource_group.aks_rg.name
     dns_prefix          = "todoapp"

     default_node_pool {
       name       = "default"
       node_count = var.node_count
       vm_size    = var.vm_size
     }

     identity {
       type = "SystemAssigned"
     }

     oms_agent {
       log_analytics_workspace_id      = azurerm_log_analytics_workspace.test.id
       msi_auth_for_monitoring_enabled = true
     }
   }

   resource "azurerm_log_analytics_workspace" "test" {
     name                = "todo-log-analytics"
     location            = azurerm_resource_group.aks_rg.location
     resource_group_name = azurerm_resource_group.aks_rg.name
     sku                 = "PerGB2018"
     retention_in_days   = 30
   }

   variable "location" {
     description = "Azure region for resources"
     type        = string
     default     = "East US"
   }

   variable "node_count" {
     description = "Number of nodes in the node pool"
     type        = number
     default     = 3
   }

   variable "vm_size" {
     description = "VM size for cluster nodes"
     type        = string
     default     = "Standard_D2s_v3"
   }

   output "client_certificate" {
     value     = azurerm_kubernetes_cluster.aks_cluster.kube_config.0.client_certificate
     sensitive = true
   }

   output "host" {
     value = azurerm_kubernetes_cluster.aks_cluster.kube_config.0.host
   }

   output "cluster_username" {
     value = azurerm_kubernetes_cluster.aks_cluster.kube_config.0.username
   }

   output "cluster_password" {
     value     = azurerm_kubernetes_cluster.aks_cluster.kube_config.0.password
     sensitive = true
   }

   output "kube_config" {
     value     = azurerm_kubernetes_cluster.aks_cluster.kube_config_raw
     sensitive = true
   }
   ```

## Next Steps

After completing this quickstart guide, you will have:

1. A local development environment with Minikube and Dapr
2. Kafka integration for event streaming
3. A basic CI/CD pipeline with GitHub Actions
4. Monitoring setup with Prometheus
5. Cloud preparation with infrastructure as code templates

The next steps would be to:

1. Deploy your actual application services to the local Kubernetes cluster
2. Enhance the CI/CD pipeline with additional checks and deployment stages
3. Set up proper secrets management for sensitive configuration
4. Prepare for cloud deployment by provisioning the infrastructure
5. Migrate from local Kafka to a managed cloud solution