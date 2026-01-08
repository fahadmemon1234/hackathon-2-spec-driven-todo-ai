from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import tasks
from routes.auth import router as auth_router
from routes.chat import router as chat_router
from db import create_db_and_tables
from mcp_server import mcp

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan, title="Todo Backend API", version="1.0.0")

# Setup CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://todo-full-stack-web-application-cha.vercel.app", "http://localhost:3000", "http://localhost:3001"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the auth, tasks, and chat routers
app.include_router(auth_router, prefix="/api")
app.include_router(tasks.router, prefix="/api")
app.include_router(chat_router, prefix="/api")

# Mount the MCP server
app.mount("/mcp", mcp.streamable_http_app())

@app.get("/")
def read_root():
    return {"message": "Phase 2 Backend Running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}