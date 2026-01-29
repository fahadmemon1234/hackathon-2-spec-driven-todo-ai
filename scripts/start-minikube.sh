#!/bin/bash

# Script to start Minikube with appropriate resources for the Todo Application with Dapr
# This script allocates sufficient resources to run all services (backend, frontend, Kafka, Redis, PostgreSQL, Dapr)

echo "Starting Minikube with resources for Todo Application + Dapr..."

# Start Minikube with Docker driver and sufficient resources
# Using 6GB RAM and 4 CPUs to accommodate all services including Dapr sidecars
minikube start \
  --driver=docker \
  --memory=6144mb \
  --cpus=4 \
  --disk-size=10gb \
  --kubernetes-version=latest

if [ $? -eq 0 ]; then
  echo "Minikube started successfully!"
  echo "Current status:"
  minikube status
  
  echo "Current nodes:"
  kubectl get nodes
else
  echo "Failed to start Minikube"
  exit 1
fi

echo "Setting up Dapr in Kubernetes mode..."
dapr init -k

if [ $? -eq 0 ]; then
  echo "Dapr initialized in Kubernetes mode successfully!"
  echo "Dapr system pods:"
  kubectl get pods -n dapr-system
else
  echo "Failed to initialize Dapr in Kubernetes mode"
  exit 1
fi

echo "Minikube setup complete with Dapr!"
echo "You can now deploy the Todo Application with Dapr integration."