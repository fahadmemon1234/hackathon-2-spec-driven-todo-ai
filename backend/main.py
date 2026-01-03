from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import tasks
from routes.auth import router as auth_router
from db import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan, title="Todo Backend API", version="1.0.0")

# Setup CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://todo-full-stack-web-application-theta.vercel.app", "http://localhost:3000"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the auth and tasks routers
app.include_router(auth_router, prefix="/api")
app.include_router(tasks.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Phase 2 Backend Running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}