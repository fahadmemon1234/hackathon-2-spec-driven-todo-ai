from sqlmodel import create_engine, Session, SQLModel
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "")

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
    SQLModel.metadata.create_all(engine)
