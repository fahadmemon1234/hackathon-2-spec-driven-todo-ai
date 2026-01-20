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


def add_task(
    user_id: str,
    title: str,
    description: str | None = None,
    priority: str = "medium",
    tags: list[str] | None = None,
    due_date: str | None = None,
    is_recurring: bool = False,
    recurrence_rule: str | None = None
) -> dict:
    from datetime import datetime
    from typing import cast

    # Convert due_date string to datetime if provided
    due_datetime = None
    if due_date:
        try:
            due_datetime = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
        except ValueError:
            raise ValueError(f"Invalid due_date format: {due_date}. Expected ISO format.")

    with get_db_session() as session:
        task = Task(
            user_id=user_id,
            title=title,
            description=description,
            completed=False,
            priority=priority,
            tags=tags or [],
            due_date=due_datetime,
            is_recurring=is_recurring,
            recurrence_rule=recurrence_rule,
            next_occurrence=None  # Will be calculated if it's a recurring task
        )

        # If it's a recurring task, calculate the next occurrence
        if task.is_recurring and task.recurrence_rule and task.due_date:
            from utils.recurrence_utils import calculate_next_occurrence
            next_occurrence = calculate_next_occurrence(task.recurrence_rule, task.due_date)
            task.next_occurrence = next_occurrence

        session.add(task)
        session.commit()
        session.refresh(task)

        # Publish task created event
        from utils.event_publisher import EventPublisher
        publisher = EventPublisher()
        try:
            publisher.publish_task_event("created", task, user_id)

            # If the task has a due date, publish a reminder event
            if task.due_date:
                publisher.publish_reminder_event(task, user_id)
        finally:
            publisher.close()

        return {
            "task_id": task.id,
            "status": "created",
            "title": task.title,
            "description": task.description,
            "priority": task.priority,
            "tags": task.tags,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "is_recurring": task.is_recurring,
            "recurrence_rule": task.recurrence_rule,
            "next_occurrence": task.next_occurrence.isoformat() if task.next_occurrence else None
        }


def list_tasks(
    user_id: str,
    status: str = "all",
    priority: str | None = None,
    tags: list[str] | None = None,
    q: str | None = None,
    sort: str = "created",
    due_after: str | None = None,
    due_before: str | None = None
) -> list:
    from datetime import datetime
    from sqlmodel import func
    from sqlalchemy import or_, and_

    with get_db_session() as session:
        query = select(Task).where(Task.user_id == user_id)

        # Status filter
        if status == "pending":
            query = query.where(Task.completed == False)
        elif status == "completed":
            query = query.where(Task.completed == True)

        # Priority filter - can accept multiple priorities
        if priority:
            priority_list = priority.split(',')
            query = query.where(Task.priority.in_(priority_list))

        # Tags filter - can accept multiple tags
        if tags:
            for tag in tags:
                query = query.where(Task.tags.op('?')(tag.strip()))

        # Search in title and description
        if q:
            search_term = f"%{q}%"
            query = query.where(or_(Task.title.ilike(search_term), Task.description.ilike(search_term)))

        # Due date range filter
        if due_after:
            try:
                due_after_date = datetime.strptime(due_after, "%Y-%m-%d").date()
                query = query.where(func.date(Task.due_date) >= due_after_date)
            except ValueError:
                raise ValueError(f"Invalid due_after date format: {due_after}. Expected YYYY-MM-DD.")

        if due_before:
            try:
                due_before_date = datetime.strptime(due_before, "%Y-%m-%d").date()
                query = query.where(func.date(Task.due_date) <= due_before_date)
            except ValueError:
                raise ValueError(f"Invalid due_before date format: {due_before}. Expected YYYY-MM-DD.")

        # Sorting - can accept multiple sort fields
        sort_fields = sort.split(',')
        order_clauses = []

        for sort_field in sort_fields:
            field_desc = sort_field.startswith('-')
            clean_field = sort_field.lstrip('-')

            if clean_field == "title":
                order_clause = Task.title.desc() if field_desc else Task.title.asc()
            elif clean_field == "priority":
                # Sort by priority: urgent, high, medium, low
                from sqlmodel import case
                priority_order = case(
                    [(Task.priority == "urgent", 1), (Task.priority == "high", 2),
                     (Task.priority == "medium", 3), (Task.priority == "low", 4)],
                    else_=5
                )
                order_clause = priority_order.desc() if field_desc else priority_order.asc()
            elif clean_field == "due_date":
                order_clause = Task.due_date.desc() if field_desc else Task.due_date.asc()
            elif clean_field == "created_at":
                order_clause = Task.created_at.desc() if field_desc else Task.created_at.asc()
            else:  # default "created" → newest first
                order_clause = Task.created_at.desc() if field_desc else Task.created_at.asc()

            order_clauses.append(order_clause)

        query = query.order_by(*order_clauses)

        tasks = session.exec(query).all()
        return [
            {
                "id": t.id,
                "title": t.title,
                "description": t.description,
                "completed": t.completed,
                "created_at": t.created_at.isoformat() if t.created_at else None,
                "priority": t.priority,
                "tags": t.tags,
                "due_date": t.due_date.isoformat() if t.due_date else None,
                "is_recurring": t.is_recurring,
                "recurrence_rule": t.recurrence_rule,
                "next_occurrence": t.next_occurrence.isoformat() if t.next_occurrence else None
            } for t in tasks
        ]


def update_task(
    user_id: str,
    task_id: int,
    title: str | None = None,
    description: str | None = None,
    priority: str | None = None,
    tags: list[str] | None = None,
    due_date: str | None = None,
    is_recurring: bool | None = None,
    recurrence_rule: str | None = None,
    next_occurrence: str | None = None
) -> dict:
    from datetime import datetime

    with get_db_session() as session:
        task = session.exec(select(Task).where(Task.id == task_id).where(Task.user_id == user_id)).first()
        if not task:
            raise ValueError(f"Task with ID {task_id} not found or does not belong to user")

        # Update task fields only if they're provided in the request
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if priority is not None:
            task.priority = priority
        if tags is not None:
            task.tags = tags
        if due_date is not None:
            try:
                task.due_date = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
            except ValueError:
                raise ValueError(f"Invalid due_date format: {due_date}. Expected ISO format.")
        if is_recurring is not None:
            task.is_recurring = is_recurring
        if recurrence_rule is not None:
            task.recurrence_rule = recurrence_rule
        if next_occurrence is not None:
            try:
                task.next_occurrence = datetime.fromisoformat(next_occurrence.replace('Z', '+00:00'))
            except ValueError:
                raise ValueError(f"Invalid next_occurrence format: {next_occurrence}. Expected ISO format.")

        # If it's a recurring task, calculate the next occurrence
        if task.is_recurring and task.recurrence_rule and task.due_date:
            from utils.recurrence_utils import calculate_next_occurrence
            next_occurrence_calc = calculate_next_occurrence(task.recurrence_rule, task.due_date)
            task.next_occurrence = next_occurrence_calc

        session.add(task)
        session.commit()
        session.refresh(task)

        # Publish task updated event
        from utils.event_publisher import EventPublisher
        publisher = EventPublisher()
        try:
            publisher.publish_task_event("updated", task, user_id)

            # If the task has a due date, publish a reminder event
            if task.due_date:
                publisher.publish_reminder_event(task, user_id)
        finally:
            publisher.close()

        return {
            "task_id": task.id,
            "status": "updated",
            "title": task.title,
            "priority": task.priority,
            "tags": task.tags,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "is_recurring": task.is_recurring,
            "recurrence_rule": task.recurrence_rule,
            "next_occurrence": task.next_occurrence.isoformat() if task.next_occurrence else None
        }


def complete_task(user_id: str, task_id: int) -> dict:
    from datetime import datetime

    with get_db_session() as session:
        task = session.exec(select(Task).where(Task.id == task_id).where(Task.user_id == user_id)).first()
        if not task:
            raise ValueError(f"Task with ID {task_id} not found or does not belong to user")

        task.completed = True

        # If this is a recurring task, we need to create the next instance
        if task.is_recurring and task.recurrence_rule:
            from utils.recurrence_utils import calculate_next_occurrence
            # Calculate the next occurrence based on the recurrence rule
            if task.next_occurrence:
                next_date = task.next_occurrence
            elif task.due_date:
                next_date = calculate_next_occurrence(task.recurrence_rule, task.due_date)
            else:
                next_date = calculate_next_occurrence(task.recurrence_rule, datetime.utcnow())

            if next_date:
                # Create the next instance of the recurring task
                next_task = Task(
                    user_id=task.user_id,
                    title=task.title,
                    description=task.description,
                    priority=task.priority,
                    tags=task.tags,
                    due_date=next_date,
                    is_recurring=task.is_recurring,
                    recurrence_rule=task.recurrence_rule,
                    completed=False,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )

                # Calculate the next occurrence for the new task
                if task.recurrence_rule:
                    next_occurrence = calculate_next_occurrence(task.recurrence_rule, next_date)
                    next_task.next_occurrence = next_occurrence

                session.add(next_task)
                session.commit()

                # Publish task created event for the new recurring instance
                from utils.event_publisher import EventPublisher
                publisher = EventPublisher()
                try:
                    publisher.publish_task_event("created", next_task, user_id)

                    # If the next task has a due date, publish a reminder event
                    if next_task.due_date:
                        publisher.publish_reminder_event(next_task, user_id)
                finally:
                    publisher.close()

        session.add(task)
        session.commit()
        session.refresh(task)

        # Publish task completed event
        from utils.event_publisher import EventPublisher
        publisher = EventPublisher()
        try:
            publisher.publish_task_event("completed", task, user_id)
        finally:
            publisher.close()

        return {
            "task_id": task.id,
            "status": "completed",
            "title": task.title,
            "next_instance_created": task.is_recurring and task.recurrence_rule
        }


def delete_task(user_id: str, task_id: int) -> dict:
    with get_db_session() as session:
        task = session.exec(select(Task).where(Task.id == task_id).where(Task.user_id == user_id)).first()
        if not task:
            raise ValueError(f"Task with ID {task_id} not found or does not belong to user")
        session.delete(task)
        session.commit()
        return {"task_id": task.id, "status": "deleted", "title": task.title}
