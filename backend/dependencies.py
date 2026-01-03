from fastapi import Header, HTTPException, Depends
from jose import JWTError, jwt
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_current_user_id(Authorization: str = Header(...)) -> str:
    """
    Dependency to extract and verify JWT from Bearer header
    Returns authenticated user_id (str UUID)
    """
    if not Authorization or not Authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization header. Expected: Bearer <token>"
        )

    token = Authorization.split(" ")[1]
    secret = os.getenv("BETTER_AUTH_SECRET")
    if not secret:
        raise RuntimeError("BETTER_AUTH_SECRET not set in .env")

    try:
        payload = jwt.decode(
            token,
            secret,
            algorithms=["HS256"]
        )

        # Extract user_id safely from common Better Auth payload structures
        user_id: str | None = None
        if "user" in payload and isinstance(payload["user"], dict):
            user_id = payload["user"].get("id")
        elif "id" in payload:
            user_id = payload.get("id")

        if not user_id or not isinstance(user_id, str):
            raise HTTPException(status_code=401, detail="Invalid token: missing user ID")

        return user_id
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token")