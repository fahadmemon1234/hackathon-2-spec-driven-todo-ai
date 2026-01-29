from sqlmodel import create_engine, Session, SQLModel
from config import DATABASE_URL
import os

if not DATABASE_URL:
    print("WARNING: DATABASE_URL not set in environment or secrets")
    # Fallback to a default SQLite database if not set
    DATABASE_URL = "sqlite:///./todo_app_default.db"
    print(f"Using fallback database: {DATABASE_URL}")

engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    future=True
)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    # Import models to register them with SQLModel metadata
    from models import Task, Conversation, Message, User
    try:
        SQLModel.metadata.create_all(engine)
        print("Database tables created successfully")
    except Exception as e:
        print(f"ERROR creating database tables: {str(e)}")
        raise
