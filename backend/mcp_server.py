from models import Task
from db import get_session
from sqlmodel import select
from contextlib import contextmanager


@contextmanager
def get_db_session():
    try:
        session_gen = get_session()
        session = next(session_gen)
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def add_task(user_id: str, title: str, description: str | None = None) -> dict:
    with get_db_session() as session:
        task = Task(user_id=user_id, title=title, description=description, completed=False)
        session.add(task)
        session.commit()
        session.refresh(task)
        return {"task_id": task.id, "status": "created", "title": task.title, "description": task.description}


def list_tasks(user_id: str, status: str = "all") -> list:
    with get_db_session() as session:
        query = select(Task).where(Task.user_id == user_id)
        if status == "pending":
            query = query.where(Task.completed == False)
        elif status == "completed":
            query = query.where(Task.completed == True)
        tasks = session.exec(query).all()
        return [
            {
                "id": t.id,
                "title": t.title,
                "description": t.description,
                "completed": t.completed,
                "created_at": t.created_at.isoformat() if t.created_at else None
            } for t in tasks
        ]


def update_task(user_id: str, task_id: int, title: str | None = None, description: str | None = None) -> dict:
    with get_db_session() as session:
        task = session.exec(select(Task).where(Task.id == task_id).where(Task.user_id == user_id)).first()
        if not task:
            raise ValueError(f"Task with ID {task_id} not found or does not belong to user")
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        session.add(task)
        session.commit()
        session.refresh(task)
        return {"task_id": task.id, "status": "updated", "title": task.title}


def complete_task(user_id: str, task_id: int) -> dict:
    with get_db_session() as session:
        task = session.exec(select(Task).where(Task.id == task_id).where(Task.user_id == user_id)).first()
        if not task:
            raise ValueError(f"Task with ID {task_id} not found or does not belong to user")
        task.completed = True
        session.add(task)
        session.commit()
        session.refresh(task)
        return {"task_id": task.id, "status": "completed", "title": task.title}


def delete_task(user_id: str, task_id: int) -> dict:
    with get_db_session() as session:
        task = session.exec(select(Task).where(Task.id == task_id).where(Task.user_id == user_id)).first()
        if not task:
            raise ValueError(f"Task with ID {task_id} not found or does not belong to user")
        session.delete(task)
        session.commit()
        return {"task_id": task.id, "status": "deleted", "title": task.title}
