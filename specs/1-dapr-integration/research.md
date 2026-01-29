# Research Findings for Dapr Integration

## Decision: Dapr Runtime Installation Method
- Rationale: Using Dapr's standalone mode for local development is simpler and doesn't require Kubernetes. This fits the requirement of using Docker Compose without Kubernetes/Minikube.
- Alternatives considered: Installing via Helm charts for Kubernetes, using Dapr in containers only without standalone runtime

## Decision: Component Configuration Approach
- Rationale: Using YAML files for Dapr component definitions is the standard approach and allows for easy configuration management and version control.
- Alternatives considered: Configuring components programmatically, using environment variables only

## Decision: Secrets Management Strategy
- Rationale: Using Dapr's local file secret store for development aligns with the requirement of "local-only" secrets without cloud secret stores.
- Alternatives considered: Using environment variables directly, using Docker secrets

## Decision: Kafka Topic Naming Convention
- Rationale: Simple, descriptive names that clearly indicate the purpose of each topic make the system easier to understand and maintain.
- Alternatives considered: Using prefixed topics, using UUID-based topic names

## Decision: State Key Structure
- Rationale: Using a consistent pattern with entity type followed by ID makes it easy to organize and retrieve state information.
- Alternatives considered: Using composite keys, using flat namespace with delimited keys