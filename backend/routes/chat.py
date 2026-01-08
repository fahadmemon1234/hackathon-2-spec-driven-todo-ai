from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from models import Conversation, Message, Task
from db import get_session
from sqlmodel import Session, select
from datetime import datetime
import os
import json

router = APIRouter()

from mcp_server import add_task, list_tasks, update_task, complete_task, delete_task

# --- Helper Functions ---

def extract_task_title(message: str) -> Optional[str]:
    text = message.lower()
    phrases = [
        "add a task to", "add task to", "create a task to", "create task to",
        "add task", "add a task", "create task", "create a task"
    ]
    for p in phrases:
        if p in text:
            title = text.replace(p, "", 1).strip()
            return title if title else None
    return None

def get_fallback_response(message: str, user_id: str, session):
    """
    Fallback rule-based responses if AI API fails.
    Returns a dict with response + optional tool_calls.
    """
    message_lower = message.lower()

    if "add" in message_lower or "create" in message_lower:
        title = extract_task_title(message)
        if not title:
            return "Please tell me what task you want to add."
        # Add to DB
        task = Task(user_id=user_id, title=title, completed=False)
        session.add(task)
        session.commit()
        return {
            "response": f"Task '{title}' has been added successfully.",
            "tool_calls": [
                {
                    "name": "add_task",
                    "arguments": {"user_id": user_id, "title": title}
                }
            ]
        }

    elif "update" in message_lower or "change" in message_lower:
         import re
         # Expecting format like "Update task 26 to call the client"
         match = re.search(r'task (\d+).*?to (.+)', message_lower)
         if not match:
             return "Please provide task ID and the new title to update."
         task_id = int(match.group(1))
         new_title = match.group(2).strip()
         if not new_title:
             return "Please provide a valid new title for the task."
         # Update using mcp_server
         result = update_task(user_id=user_id, task_id=task_id, title=new_title)
         return {
             "response": f"Task '{new_title}' has been updated successfully.",
             "tool_calls": [
                 {
                     "name": "update_task",
                     "arguments": {"user_id": user_id, "task_id": task_id, "title": new_title}
                 }
             ]
         }

    elif "show" in message_lower or "list" in message_lower or "my tasks" in message_lower:
        tasks = session.exec(select(Task).where(Task.user_id == user_id)).all()
        if tasks:
            task_list = "\n".join([f"- {task.id}: {task.title} [{'x' if task.completed else ' '}] " for task in tasks])
            return {
                "response": f"Here are your tasks:\n{task_list}",
                "tool_calls": [
                    {
                        "name": "list_tasks",
                        "arguments": {"user_id": user_id}
                    }
                ]
            }
        else:
            return {
                "response": "You don't have any tasks yet. Add one like 'Add a task to buy groceries'.",
                "tool_calls": [
                    {
                        "name": "list_tasks",
                        "arguments": {"user_id": user_id}
                    }
                ]
            }


    elif "complete" in message_lower or "done" in message_lower or "finish" in message_lower:
        import re
        match = re.search(r'task (\d+)', message_lower)
        if not match:
            return {
                "response": "Please provide the task ID to mark as complete.",
                "tool_calls": []
            }
        
        task_id = int(match.group(1))
        
        try:
            result = complete_task(user_id=user_id, task_id=task_id)
            return {
                "response": f"Task {task_id} has been marked as complete.",
                "tool_calls": [
                    {
                        "name": "complete_task",
                        "arguments": {"user_id": user_id, "task_id": task_id}
                    }
                ]
            }
        except Exception as e:
            # Catch database errors, missing task, etc.
            return {
                "response": f"Could not complete task {task_id}. It may not exist.",
                "tool_calls": []
            }


    elif "delete" in message_lower or "remove" in message_lower:
        import re
        match = re.search(r'task (\d+)', message_lower)
        if not match:
            return {
                "response": "Please provide the task ID to delete.",
                "tool_calls": []
            }
        task_id = int(match.group(1))
        result = delete_task(user_id=user_id, task_id=task_id)
        return {
            "response": f"Task {task_id} has been deleted successfully.",
            "tool_calls": [
                {
                    "name": "delete_task",
                    "arguments": {"user_id": user_id, "task_id": task_id}
                }
            ]
        }

    elif "hello" in message_lower or "hi" in message_lower or "hey" in message_lower:
        return {
            "response": "Hello! I can help manage your tasks. Say 'Add a task', 'Update task', 'Show my tasks', etc.",
            "tool_calls": []
        }

    # --- DEFAULT ---
    else:
        return {
            "response": f"I received your message: '{message}'. Try 'Add a task', 'Update task', or 'Show my tasks'.",
            "tool_calls": []
        }

# --- Request / Response Models ---

class ChatRequest(BaseModel):
    conversation_id: Optional[int] = None
    message: str

class ToolCall(BaseModel):
    name: str
    arguments: dict

class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    tool_calls: Optional[List[ToolCall]] = None

# --- System Prompt ---

SYSTEM_PROMPT_TEMPLATE = """You are an AI Task Management Assistant. Your job is to read a user's message and respond with structured JSON for managing tasks. Always use the following tool calls instead of plain text.

Available tools: add_task, update_task, complete_task, delete_task, list_tasks.

Always return JSON in this format:

{{
  "response": "<short confirmation>",
  "tool_calls": [{{ "name": "<tool>", "arguments": {{ ... }} }}]
}}

Current date: {current_date}
"""

def get_system_prompt(user_id: str):
    prompt = SYSTEM_PROMPT_TEMPLATE.format(current_date=datetime.now().strftime("%Y-%m-%d"))
    prompt = prompt.replace("USER123", f'"{user_id}"')
    return prompt

# --- Chat Endpoint ---

@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat(user_id: str, request: ChatRequest, session: Session = Depends(get_session)):
    try:
        # --- Get or create conversation ---
        conversation = None
        if request.conversation_id:
            conversation = session.exec(
                select(Conversation).where(Conversation.id == request.conversation_id).where(Conversation.user_id == user_id)
            ).first()
            if not conversation:
                raise HTTPException(status_code=404, detail="Conversation not found")
        else:
            conversation = Conversation(user_id=user_id)
            session.add(conversation)
            session.commit()
            session.refresh(conversation)

        # --- Store user message ---
        user_message = Message(conversation_id=conversation.id, role="user", content=request.message)
        session.add(user_message)
        session.commit()

        # --- Fallback logic --- 
        # For now, we always use fallback; AI integration can be added later
        fallback_result = get_fallback_response(request.message, user_id, session)
        if isinstance(fallback_result, dict):
            response_text = fallback_result["response"]
            processed_tool_calls = [ToolCall(**tc) for tc in fallback_result.get("tool_calls", [])]
        else:
            response_text = fallback_result
            processed_tool_calls = []

        # --- Store assistant message ---
        assistant_message = Message(conversation_id=conversation.id, role="assistant", content=response_text)
        session.add(assistant_message)
        session.commit()

        return ChatResponse(
            conversation_id=conversation.id,
            response=response_text,
            tool_calls=processed_tool_calls if processed_tool_calls else None
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
