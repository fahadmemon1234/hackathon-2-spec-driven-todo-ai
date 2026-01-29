# Data Model: Cloud & Infrastructure Components

**Feature**: 19-cloud-infrastructure-specification
**Created**: 2026-01-28
**Status**: Complete
**Author**: Qwen AI

## Overview

This document defines the data models for the cloud infrastructure components including Kubernetes cluster configuration, Dapr components, Kafka topics, and monitoring configurations.

## 1. Kubernetes Cluster Configuration

### Cluster Definition
- **Name**: String (unique identifier)
- **Provider**: Enum (AKS, GKE, OKE, Minikube)
- **Region**: String (cloud region or local)
- **NodeCount**: Integer (minimum 1 for Minikube, 3+ for cloud)
- **NodeSize**: String (VM size/type)
- **ResourceLimits**: Object
  - CPU: String (e.g., "4", "4000m")
  - Memory: String (e.g., "8Gi", "8192Mi")
- **NetworkPolicy**: String (configuration for network isolation)
- **CreatedAt**: DateTime (timestamp of creation)
- **Status**: Enum (Pending, Running, Stopped, Failed)

### Namespace Configuration
- **Name**: String (namespace identifier)
- **Environment**: Enum (Development, Staging, Production)
- **ResourceQuota**: Object
  - Limits: Object (CPU, Memory constraints)
  - Requests: Object (CPU, Memory constraints)
- **NetworkPolicy**: String (network rules)
- **Labels**: Map<String, String> (key-value pairs for identification)

## 2. Dapr Configuration

### Component Definition
- **Name**: String (unique component name)
- **Type**: Enum (statestore, pubsub, secretstore, configuration)
- **Version**: String (component version)
- **Metadata**: Array<Object>
  - Name: String (metadata property name)
  - Value: String (metadata property value)
  - SecretKeyRef: Object (reference to secret if applicable)
- **Scopes**: Array<String> (list of applications that can use this component)
- **InitTimeout**: String (timeout duration for initialization)

### State Store Component
- **Component Properties** (inherits from Component Definition)
- **ActorStateStore**: Boolean (whether this store is used for actor state)
- **Transactional**: Boolean (whether transactional operations are supported)
- **TTLInSeconds**: Integer (time-to-live for state entries)

### Pub/Sub Component
- **Component Properties** (inherits from Component Definition)
- **ConsumerID**: String (identifier for consumer group)
- **DisableEntityManagement**: Boolean (whether to disable topic/queue creation)
- **MaxRetries**: Integer (maximum number of retry attempts)

### Secret Store Component
- **Component Properties** (inherits from Component Definition)
- **IncludeConnectionDetailsInException**: Boolean (whether to include connection details in exceptions)

## 3. Kafka Configuration

### Topic Definition
- **Name**: String (unique topic identifier)
- **Partitions**: Integer (number of partitions)
- **ReplicationFactor**: Integer (number of replicas)
- **RetentionMs**: Integer (retention period in milliseconds)
- **CleanupPolicy**: Enum (compact, delete, compact,delete)
- **CompressionType**: Enum (gzip, snappy, lz4, zstd, uncompressed)
- **MaxMessageBytes**: Integer (maximum message size in bytes)

### Consumer Group
- **GroupId**: String (unique identifier for consumer group)
- **Topics**: Array<String> (list of subscribed topics)
- **AutoOffsetReset**: Enum (earliest, latest)
- **EnableAutoCommit**: Boolean (whether to auto-commit offsets)
- **SessionTimeoutMs**: Integer (session timeout in milliseconds)

### Producer Configuration
- **ClientId**: String (identifier for producer client)
- **Acks**: Enum (0, 1, all) (acknowledgment level)
- **Retries**: Integer (number of retry attempts)
- **BatchSize**: Integer (batch size in bytes)
- **LingerMs**: Integer (linger time in milliseconds)
- **BufferMemory**: Integer (buffer memory in bytes)

## 4. Monitoring Configuration

### Metric Definition
- **Name**: String (metric identifier)
- **Description**: String (human-readable description)
- **Type**: Enum (gauge, counter, histogram, summary)
- **Labels**: Array<String> (list of label names)
- **Query**: String (Prometheus query for the metric)

### Dashboard Panel
- **Title**: String (panel title)
- **Description**: String (optional description)
- **Type**: Enum (graph, singlestat, table, heatmap)
- **Targets**: Array<Object>
  - Expr: String (Prometheus query expression)
  - LegendFormat: String (legend format)
- **GridPos**: Object
  - h: Integer (height in grid units)
  - w: Integer (width in grid units)
  - x: Integer (x coordinate)
  - y: Integer (y coordinate)

### Alert Rule
- **Alert**: String (alert name)
- **Expr**: String (Prometheus query that triggers alert)
- **For**: String (duration to wait before firing)
- **Labels**: Map<String, String> (key-value pairs for categorization)
- **Annotations**: Map<String, String> (descriptive information)

## 5. CI/CD Configuration

### Workflow Definition
- **Name**: String (workflow identifier)
- **On**: Object
  - Push: Object (branches to trigger on push)
  - PullRequest: Object (branches to trigger on PR)
- **Jobs**: Array<Object>
  - Name: String (job identifier)
  - RunsOn: String (runner environment)
  - Steps: Array<Object>
    - Name: String (step identifier)
    - Uses: String (action to use)
    - Run: String (command to run)
    - Env: Map<String, String> (environment variables)

### Deployment Configuration
- **Environment**: String (target environment)
- **Branch**: String (source branch)
- **Variables**: Map<String, String> (deployment variables)
- **Approvals**: Integer (number of required approvals)

## Relationships

### Kubernetes Cluster to Namespaces
- One cluster contains many namespaces
- Each namespace belongs to one cluster

### Dapr Components to Applications
- Many Dapr components can be used by many applications (many-to-many via scopes)

### Kafka Topics to Consumers/Producers
- One topic can have many consumers and producers
- Consumers and producers connect to many topics

### Metrics to Dashboards
- Many metrics can be displayed on many dashboards
- Dashboards aggregate multiple metrics