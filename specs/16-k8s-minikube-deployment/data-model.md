# Data Model: Local Kubernetes Deployment for Todo Chatbot Application

## Kubernetes Resources

### ConfigMap
- **Name**: `todo-app-config`
- **Purpose**: Store configuration values for frontend and backend
- **Fields**:
  - `NEXT_PUBLIC_API_URL`: Backend API URL for frontend
  - `DATABASE_URL`: Database connection string
  - `AUTH_SECRET`: Authentication secret

### Secret
- **Name**: `todo-app-secrets`
- **Purpose**: Store sensitive configuration values
- **Fields**:
  - `auth_secret`: Authentication secret
  - `database_password`: Database password
  - `openai_api_key`: API key for OpenAI integration

### PersistentVolumeClaim (if needed)
- **Name**: `todo-app-data-pvc`
- **Purpose**: Persistent storage for database
- **Fields**:
  - `storage`: 1Gi
  - `accessModes`: ["ReadWriteOnce"]

## Deployments

### Frontend Deployment
- **Name**: `todo-frontend`
- **Replicas**: 1 (for local development)
- **Container**:
  - Image: `todo-frontend:local`
  - Port: 3000
  - Environment variables from ConfigMap and Secret

### Backend Deployment
- **Name**: `todo-backend`
- **Replicas**: 1 (for local development)
- **Container**:
  - Image: `todo-backend:local`
  - Port: 8000
  - Environment variables from ConfigMap and Secret

## Services

### Frontend Service
- **Name**: `todo-frontend-service`
- **Type**: ClusterIP or NodePort
- **Port**: 3000
- **Target Port**: 3000

### Backend Service
- **Name**: `todo-backend-service`
- **Type**: ClusterIP
- **Port**: 8000
- **Target Port**: 8000

## Ingress (optional)
- **Name**: `todo-app-ingress`
- **Rules**:
  - Path `/` -> Frontend service
  - Path `/api/` -> Backend service

## Helm Values Structure
- **frontend.image.repository**: Frontend image repository
- **frontend.image.tag**: Frontend image tag
- **frontend.service.port**: Frontend service port
- **backend.image.repository**: Backend image repository
- **backend.image.tag**: Backend image tag
- **backend.service.port**: Backend service port
- **config.api_url**: API URL configuration
- **ingress.enabled**: Enable/disable ingress
- **ingress.hosts**: Hostnames for ingress