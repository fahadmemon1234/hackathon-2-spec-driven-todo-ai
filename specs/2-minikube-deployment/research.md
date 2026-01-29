# Research Findings for Minikube Deployment

## Minikube Resource Requirements

**Decision**: Recommended minimum resources for Minikube cluster
**Rationale**: The Todo Application with Dapr integration requires sufficient resources to run all services (backend, Kafka, Redis, PostgreSQL, Zookeeper, Dapr system services)
**Findings**:
- Minikube requires at least 4GB RAM and 2 CPU cores for basic operation
- For the full application stack with Dapr, recommend 6GB+ RAM and 4+ CPU cores
- Disk space requirement is approximately 10GB for images and persistent data
- Swap space should be available if running on systems with limited RAM

**Alternatives considered**:
- Using lighter-weight alternatives to Kafka (NATS, RabbitMQ) - rejected as it would change the architecture
- Using Minikube's resource constraints to limit usage - decided against as it may impact performance

## Dapr Kubernetes Best Practices

**Decision**: Use Dapr in Kubernetes mode with proper annotations and component definitions
**Rationale**: Dapr's Kubernetes mode provides better integration with Kubernetes native features and follows recommended practices
**Findings**:
- Use `dapr.io` annotations in pod specs for sidecar injection
- Deploy Dapr components as Kubernetes CRDs (Custom Resource Definitions)
- Use Kubernetes secrets for sensitive Dapr component configurations
- Enable mTLS for service-to-service communication in production

**Alternatives considered**:
- Standalone Dapr mode in Kubernetes - rejected as it's not the recommended approach for Kubernetes
- Manual sidecar deployment - rejected as annotation-based injection is simpler and more reliable

## Image Management Strategy

**Decision**: Use Minikube's image loading feature to make local images available
**Rationale**: Minikube provides a built-in mechanism to load local Docker images without needing a registry
**Findings**:
- Use `minikube image load <image-name>` to load images into Minikube's Docker environment
- Alternatively, build images directly in Minikube's Docker environment using `eval $(minikube docker-env)`
- For development, the image loading approach is simpler and more reliable

**Alternatives considered**:
- Using a local Docker registry - more complex setup than needed
- Pushing to a public registry - security concerns with development images

## Service Exposure Options

**Decision**: Use kubectl port-forward for development and testing
**Rationale**: For local development with Minikube, port-forward provides secure and simple access to services
**Findings**:
- `kubectl port-forward` is the standard approach for accessing services during development
- Minikube also supports `minikube service` to expose services via LoadBalancer
- Ingress controllers can be enabled but are overkill for local development

**Alternatives considered**:
- NodePort services - less convenient than port-forward
- LoadBalancer services with Minikube tunnel - requires additional setup
- Ingress controllers - unnecessary complexity for local development

## Persistent Storage Options

**Decision**: Use Minikube's built-in storage provisioner for development
**Rationale**: Minikube includes a storage provisioner that creates persistent volumes dynamically
**Findings**:
- Minikube has a built-in storage provisioner that creates hostPath volumes
- For PostgreSQL and Redis, use PersistentVolumeClaims to ensure data persistence
- For production, consider using cloud-specific storage solutions

**Alternatives considered**:
- HostPath volumes directly - harder to manage than PVCs
- External storage services - unnecessary for local development