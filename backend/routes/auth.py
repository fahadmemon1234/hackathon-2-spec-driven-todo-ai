from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from sqlmodel import Session, select
from db import engine
from models import User
from dependencies import get_current_user_id
from datetime import datetime, timedelta
from jose import jwt
import os
import hashlib
from config import BETTER_AUTH_SECRET as CONFIG_BETTER_AUTH_SECRET

router = APIRouter()

# Define request models
class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

def hash_password(password: str) -> str:
    """Hash the password using SHA-256 (in production, use bcrypt or similar)"""
    return hashlib.sha256(password.encode()).hexdigest()

@router.post("/auth/signup")
async def signup(user_data: UserCreate):
    try:
        with Session(engine) as session:
            # Check if user already exists
            existing_user = session.exec(select(User).where(User.email == user_data.email)).first()
            if existing_user:
                raise HTTPException(status_code=400, detail="User already exists")

            # Hash the password
            password_hash = hash_password(user_data.password)

            # Create a new user in the database
            user = User(
                email=user_data.email,
                password_hash=password_hash
            )

            session.add(user)
            session.commit()
            session.refresh(user)

            # Generate a proper JWT token
            secret = CONFIG_BETTER_AUTH_SECRET
            if not secret:
                # Log the error for debugging
                print("ERROR: BETTER_AUTH_SECRET not set in environment or secrets")
                raise HTTPException(status_code=500, detail="Server configuration error: Authentication secret not set")

            # Create JWT payload with user information
            payload = {
                "user": {
                    "id": user.id,
                    "email": user.email
                },
                "exp": datetime.utcnow() + timedelta(days=7),  # Token expires in 7 days
                "iat": datetime.utcnow()  # Issued at time
            }

            try:
                token = jwt.encode(payload, secret, algorithm="HS256")
            except Exception as e:
                print(f"ERROR: Failed to encode JWT token: {str(e)}")
                raise HTTPException(status_code=500, detail="Authentication error: Failed to generate token")

            return {
                "user": {
                    "id": user.id,
                    "email": user.email
                },
                "token": token
            }
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Log unexpected errors
        print(f"ERROR in signup: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during signup")

@router.post("/auth/login")
async def login(user_data: UserLogin):
    try:
        with Session(engine) as session:
            # Check if user exists and password matches
            user = session.exec(select(User).where(User.email == user_data.email)).first()
            if not user or user.password_hash != hash_password(user_data.password):
                raise HTTPException(status_code=401, detail="Invalid credentials")

            # Generate a proper JWT token
            secret = CONFIG_BETTER_AUTH_SECRET
            if not secret:
                # Log the error for debugging
                print("ERROR: BETTER_AUTH_SECRET not set in environment or secrets")
                raise HTTPException(status_code=500, detail="Server configuration error: Authentication secret not set")

            # Create JWT payload with user information
            payload = {
                "user": {
                    "id": user.id,
                    "email": user.email
                },
                "exp": datetime.utcnow() + timedelta(days=7),  # Token expires in 7 days
                "iat": datetime.utcnow()  # Issued at time
            }

            try:
                token = jwt.encode(payload, secret, algorithm="HS256")
            except Exception as e:
                print(f"ERROR: Failed to encode JWT token: {str(e)}")
                raise HTTPException(status_code=500, detail="Authentication error: Failed to generate token")

            return {
                "user": {
                    "id": user.id,
                    "email": user.email
                },
                "token": token
            }
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Log unexpected errors
        print(f"ERROR in login: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during login")

@router.post("/auth/logout")
async def logout():
    # In a real implementation, we would invalidate the token
    # For now, we'll just return a success response
    return {"success": True}

@router.get("/auth/session")
async def get_session(current_user_id: str = Depends(get_current_user_id)):
    with Session(engine) as session:
        # Get the user from the database based on the user_id from JWT
        user = session.get(User, current_user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return {
            "user": {
                "id": user.id,
                "email": user.email
            }
        }