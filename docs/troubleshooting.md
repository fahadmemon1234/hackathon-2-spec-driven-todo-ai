# Troubleshooting Guide for Dapr Integration

This document provides solutions to common issues encountered when running the Dapr-integrated Todo Application.

## Common Issues and Solutions

### 1. Dapr Sidecar Not Starting

**Symptoms:**
- Application fails to start with Dapr sidecar
- Error messages about Dapr not being available
- Connection refused errors on Dapr ports

**Solutions:**
1. Verify Dapr is installed and initialized:
   ```bash
   dapr --version
   dapr list
   ```

2. If Dapr is not initialized, run:
   ```bash
   dapr init
   ```

3. Check if Dapr placement service is running:
   ```bash
   dapr uninstall
   dapr init
   ```

4. Ensure ports 3500 (HTTP) and 50001 (gRPC) are not in use by other processes

### 2. Kafka Connection Issues

**Symptoms:**
- Failed to publish/subscribe to Kafka topics
- Connection timeout errors
- "Broker not available" messages

**Solutions:**
1. Verify Kafka is running:
   ```bash
   docker-compose ps | grep kafka
   ```

2. Check Kafka logs:
   ```bash
   docker-compose logs kafka
   ```

3. Verify Kafka configuration in `components/pubsub.yaml`:
   - Brokers should match the service name in docker-compose
   - Consumer group should be unique per service

4. Test Kafka connectivity from the backend container:
   ```bash
   docker-compose exec backend bash
   # Inside container:
   telnet kafka 9092
   ```

### 3. Redis Connection Issues

**Symptoms:**
- Failed to save/retrieve state from Redis
- Connection timeout errors
- "Connection refused" messages

**Solutions:**
1. Verify Redis is running:
   ```bash
   docker-compose ps | grep redis
   ```

2. Check Redis logs:
   ```bash
   docker-compose logs redis
   ```

3. Verify Redis configuration in `components/statestore.yaml`:
   - Host should match the service name in docker-compose
   - Password should match the Redis configuration

4. Test Redis connectivity from the backend container:
   ```bash
   docker-compose exec backend bash
   # Inside container:
   redis-cli -h redis -p 6379 ping
   ```

### 4. Component Configuration Issues

**Symptoms:**
- Dapr reports component initialization failures
- Components not found in Dapr logs
- Configuration validation errors

**Solutions:**
1. Verify component files are in the correct directory:
   - Components should be in the `components/` directory
   - Files should have `.yaml` extension
   - Files should follow Dapr component schema

2. Check component file syntax:
   ```bash
   # Validate YAML syntax
   yamllint components/*.yaml
   ```

3. Verify component names match references in code:
   - Pub/sub name in code should match metadata.name in pubsub.yaml
   - State store name in code should match metadata.name in statestore.yaml

4. Check Dapr logs for specific error messages:
   ```bash
   dapr logs
   ```

### 5. Secrets Access Issues

**Symptoms:**
- Failed to retrieve secrets from Dapr
- Configuration values not loaded from secrets
- "Secret not found" errors

**Solutions:**
1. Verify secrets file exists and has correct format:
   - File should be at the path specified in secrets.yaml
   - JSON format should be valid
   - Keys should match those requested in code

2. Check secrets component configuration:
   - Verify secretsFile path is correct
   - Ensure file permissions allow Dapr to read the file

3. Test secret access:
   ```bash
   # Access secret via Dapr API
   curl http://localhost:3500/v1.0/secrets/local-secret-store/secret-key
   ```

### 6. Service Invocation Issues

**Symptoms:**
- Failed to invoke other services via Dapr
- "Service not found" errors
- Connection timeout errors

**Solutions:**
1. Verify service is running and has correct App ID:
   - Check that the target service is running
   - Verify App ID matches the one specified in service invocation

2. Check network connectivity between services:
   - Ensure services are on the same Docker network
   - Verify service names match those in docker-compose.yml

3. Test service invocation:
   ```bash
   # Invoke service via Dapr API
   curl -X POST http://localhost:3500/v1.0/invoke/backend-service/method/health
   ```

### 7. Docker Compose Issues

**Symptoms:**
- Services fail to start
- Dependency errors between services
- Port conflicts

**Solutions:**
1. Check Docker Compose configuration:
   - Verify service dependencies (depends_on)
   - Check port mappings don't conflict
   - Ensure volumes are properly mounted

2. Clean up and restart:
   ```bash
   docker-compose down
   docker-compose up -d
   ```

3. Check Docker resources:
   - Ensure sufficient memory allocated to Docker
   - Check disk space availability

4. View service logs:
   ```bash
   docker-compose logs <service-name>
   ```

### 8. Application-Specific Issues

**Symptoms:**
- Task creation fails
- Reminders not processing
- State not persisting correctly

**Solutions:**
1. Check application logs:
   ```bash
   docker-compose logs backend
   ```

2. Verify Dapr integration code:
   - Check that Dapr HTTP endpoints are correctly formatted
   - Verify state key patterns match those in the data model
   - Ensure pub/sub topic names match component configurations

3. Test individual components:
   - Manually test state operations via Dapr API
   - Manually test pub/sub via Dapr API
   - Verify cron binding triggers manually

## Debugging Tips

### 1. Enable Dapr Debug Logging
Add the following to your Dapr configuration:
```yaml
apiVersion: dapr.io/v1alpha1
kind: Configuration
metadata:
  name: dapr-config
spec:
  tracing:
    samplingRate: "1"
    zipkin:
      endpointAddress: "http://zipkin:9411/api/v2/spans"
  logging:
    logLevel: "debug"
```

### 2. Use Dapr CLI for Testing
```bash
# Check running Dapr applications
dapr list

# Get Dapr sidecar logs
dapr logs

# Test pub/sub
curl -X POST http://localhost:3500/v1.0/publish/pubsub-name/topic-name -H "Content-Type: application/json" -d '{"message": "test"}'

# Test state store
curl -X POST http://localhost:3500/v1.0/state/statestore -H "Content-Type: application/json" -d '[{ "key": "test-key", "value": "test-value"}]'
curl http://localhost:3500/v1.0/state/statestore/test-key
```

### 3. Check Dapr Health
Verify that the Dapr sidecar is healthy by checking the health endpoint of your application and ensuring it can communicate with the Dapr sidecar.

## Getting Help

If you encounter issues not covered in this guide:

1. Check the Dapr documentation: https://docs.dapr.io/
2. Review the application logs and Dapr logs for error details
3. Verify all prerequisites are met
4. Ensure all configuration files are properly formatted
5. Consult the community forums or raise an issue in the repository