from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import json

router = APIRouter()

@router.post("/invoke/{method_name}")
async def service_invoke(method_name: str, payload: Dict[Any, Any] = None):
    """
    Generic service invocation endpoint that allows other services to call
    specific methods on this service via Dapr service invocation.
    
    Args:
        method_name: The name of the method to invoke
        payload: The data to pass to the method
        
    Returns:
        The result of the method invocation
    """
    try:
        print(f"Service invocation requested for method: {method_name}")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        
        # In a real implementation, you would route to specific methods based on method_name
        # For this example, we'll just return a success message
        if method_name == "health-check":
            result = {
                "status": "healthy",
                "service": "backend-service",
                "timestamp": "",
                "details": "Service is operational"
            }
        elif method_name == "get-task-summary":
            # Example of a more complex operation
            user_id = payload.get("userId", "unknown")
            result = {
                "status": "success", 
                "summary": f"Task summary for user {user_id}",
                "tasks_count": 0,  # Would come from actual data
                "pending_tasks": 0,  # Would come from actual data
                "completed_tasks": 0  # Would come from actual data
            }
        else:
            # Unknown method
            raise HTTPException(
                status_code=404, 
                detail=f"Method '{method_name}' not found"
            )
        
        result["timestamp"] = ""
        
        print(f"Service invocation completed for method: {method_name}")
        return result
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        print(f"Error during service invocation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def service_health():
    """
    Health check endpoint for service invocation.
    This can be called by other services to check if this service is healthy.
    """
    try:
        health_status = {
            "status": "healthy",
            "service": "backend-service",
            "timestamp": "",
            "checks": {
                "database": "connected",
                "redis": "connected",  # Would check actual connection
                "kafka": "connected",  # Would check actual connection
                "dapr": "connected"     # Would check actual connection
            }
        }
        
        return health_status
    except Exception as e:
        print(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@router.get("/metadata")
async def service_metadata():
    """
    Metadata endpoint that provides information about this service.
    This can be called by other services to understand what this service offers.
    """
    try:
        metadata = {
            "serviceId": "backend-service",
            "version": "1.0.0",
            "capabilities": [
                "task-management",
                "reminder-scheduling", 
                "event-publishing",
                "state-management"
            ],
            "endpoints": [
                {
                    "method": "GET",
                    "path": "/health",
                    "description": "Service health check"
                },
                {
                    "method": "POST",
                    "path": "/invoke/{method_name}",
                    "description": "Generic service invocation"
                },
                {
                    "method": "GET", 
                    "path": "/metadata",
                    "description": "Service metadata"
                }
            ],
            "dapr": {
                "appId": "backend-service",
                "httpPort": 3500,
                "grpcPort": 50001
            }
        }
        
        return metadata
    except Exception as e:
        print(f"Metadata retrieval failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Metadata retrieval failed: {str(e)}")