import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import tasks
from routes.auth import router as auth_router
from routes.chat import router as chat_router
from routes.notifications import router as notifications_router
from routes.subscriptions import router as subscriptions_router
from routes.reminders import router as reminders_router
from routes.internal import router as internal_router
from db import create_db_and_tables
from config import load_configuration_from_secrets

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load configuration from Dapr secrets
    try:
        await load_configuration_from_secrets()
        print("Configuration loaded from Dapr secrets")
    except Exception as e:
        print(f"Error loading configuration from secrets: {e}")
        print("Continuing with default configuration...")
    
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan, title="Todo Backend with Dapr Integration", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api")
app.include_router(tasks.router, prefix="/api")
app.include_router(chat_router, prefix="/api")
app.include_router(notifications_router, prefix="/api")
app.include_router(subscriptions_router, prefix="/api")
app.include_router(reminders_router, prefix="/api")
app.include_router(internal_router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Todo Backend with Dapr Integration Running"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "dapr_integration": True}

# Include the task routes
app.include_router(tasks.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)