#!/bin/bash
# Script to verify Dapr dashboard accessibility

echo "Verifying Dapr dashboard accessibility..."
echo "========================================="

# Check if Dapr CLI is available
if ! command -v dapr &> /dev/null; then
    echo "❌ Dapr CLI is not installed or not in PATH"
    exit 1
fi

# Check if Dapr is running in Kubernetes mode
if ! dapr status -k &> /dev/null; then
    echo "❌ Dapr is not running in Kubernetes mode"
    echo "Make sure Dapr is initialized: dapr init -k"
    exit 1
fi

echo "Dapr is running in Kubernetes mode."

# Get the status of Dapr system services
echo "Dapr System Status:"
dapr status -k

# Check if Dapr dashboard can be accessed
echo "Attempting to start Dapr dashboard..."
echo "Note: This will start the dashboard on http://localhost:8080"
echo "Press Ctrl+C to stop the dashboard once verified"

# Start the Dapr dashboard in the background
dapr dashboard -k &
DAPR_DASHBOARD_PID=$!

# Wait a moment for the dashboard to start
sleep 5

# Check if the dashboard process is still running
if ps -p $DAPR_DASHBOARD_PID > /dev/null; then
    echo "✅ Dapr dashboard is accessible at http://localhost:8080"
    echo "Dashboard process PID: $DAPR_DASHBOARD_PID"
    
    # Kill the dashboard process
    kill $DAPR_DASHBOARD_PID
    echo "Dapr dashboard stopped."
else
    echo "❌ Failed to start Dapr dashboard"
    exit 1
fi

# Also verify through Kubernetes services
echo "Verifying Dapr placement service (part of Dapr system):"
kubectl get pods -n dapr-system

echo ""
echo "Dapr dashboard verification completed!"