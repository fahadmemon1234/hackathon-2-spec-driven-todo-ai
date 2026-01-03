from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import json

app = FastAPI()

@app.post("/api/auth/signup")
async def signup(request: Request):
    try:
        body = await request.json()
        email = body.get("email")
        password = body.get("password")
        
        # Validate input
        if not email or not password:
            raise HTTPException(status_code=400, detail="Email and password are required")
        
        # In a real implementation, we would create a user in the database
        # For now, we'll simulate a successful signup
        user_data = {
            "id": "user123",
            "email": email
        }
        
        # Generate a mock JWT token
        # In a real implementation, we would use the Better Auth library to generate a proper JWT
        token = "mock-jwt-token-for-testing"
        
        return JSONResponse(
            status_code=200,
            content={
                "user": user_data,
                "token": token
            }
        )
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/auth/login")
async def login(request: Request):
    try:
        body = await request.json()
        email = body.get("email")
        password = body.get("password")
        
        # Validate input
        if not email or not password:
            raise HTTPException(status_code=400, detail="Email and password are required")
        
        # In a real implementation, we would verify the user's credentials against the database
        # For now, we'll simulate a successful login
        user_data = {
            "id": "user123",
            "email": email
        }
        
        # Generate a mock JWT token
        # In a real implementation, we would use the Better Auth library to generate a proper JWT
        token = "mock-jwt-token-for-testing"
        
        return JSONResponse(
            status_code=200,
            content={
                "user": user_data,
                "token": token
            }
        )
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/auth/logout")
async def logout():
    # In a real implementation, we would invalidate the token
    # For now, we'll just return a success response
    return JSONResponse(
        status_code=200,
        content={
            "success": True
        }
    )

@app.get("/api/auth/session")
async def session(request: Request):
    # In a real implementation, we would validate the JWT token from the Authorization header
    # For now, we'll return a mock user if a token is present
    auth_header = request.headers.get("Authorization")
    
    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse(
            status_code=200,
            content={
                "user": None
            }
        )
    
    # Extract token
    token = auth_header.split(" ")[1]
    
    # In a real implementation, we would decode and validate the JWT
    # For now, we'll return a mock user
    if token:
        user_data = {
            "id": "user123",
            "email": "user@example.com"
        }
        return JSONResponse(
            status_code=200,
            content={
                "user": user_data
            }
        )
    else:
        return JSONResponse(
            status_code=200,
            content={
                "user": None
            }
        )