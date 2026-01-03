from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from sqlmodel import SQLModel as SQLModelBase, Field, Session, select
from db import engine
from dependencies import get_current_user_id
from datetime import datetime, timedelta
from jose import jwt
import os
import hashlib
import uuid

router = APIRouter()

# Define request models
class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

# Define User model for database
class User(SQLModelBase, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    email: str = Field(unique=True, index=True)
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

def hash_password(password: str) -> str:
    """Hash the password using SHA-256 (in production, use bcrypt or similar)"""
    return hashlib.sha256(password.encode()).hexdigest()

@router.post("/auth/signup")
async def signup(user_data: UserCreate):
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
        secret = os.getenv("BETTER_AUTH_SECRET")
        if not secret:
            raise RuntimeError("BETTER_AUTH_SECRET not set in .env")

        # Create JWT payload with user information
        payload = {
            "user": {
                "id": user.id,
                "email": user.email
            },
            "exp": datetime.utcnow() + timedelta(days=7),  # Token expires in 7 days
            "iat": datetime.utcnow()  # Issued at time
        }

        token = jwt.encode(payload, secret, algorithm="HS256")

        return {
            "user": {
                "id": user.id,
                "email": user.email
            },
            "token": token
        }

@router.post("/auth/login")
async def login(user_data: UserLogin):
    with Session(engine) as session:
        # Check if user exists and password matches
        user = session.exec(select(User).where(User.email == user_data.email)).first()
        if not user or user.password_hash != hash_password(user_data.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Generate a proper JWT token
        secret = os.getenv("BETTER_AUTH_SECRET")
        if not secret:
            raise RuntimeError("BETTER_AUTH_SECRET not set in .env")

        # Create JWT payload with user information
        payload = {
            "user": {
                "id": user.id,
                "email": user.email
            },
            "exp": datetime.utcnow() + timedelta(days=7),  # Token expires in 7 days
            "iat": datetime.utcnow()  # Issued at time
        }

        token = jwt.encode(payload, secret, algorithm="HS256")

        return {
            "user": {
                "id": user.id,
                "email": user.email
            },
            "token": token
        }

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