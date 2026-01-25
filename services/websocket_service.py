import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from kafka import KafkaConsumer
import threading
import uvicorn
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.user_connections: Dict[str, List[WebSocket]] = {}  # user_id -> connections mapping

    async def connect(self, websocket: WebSocket, user_id: str = None):
        await websocket.accept()
        self.active_connections.append(websocket)

        # Add to user-specific connections if user_id is provided
        if user_id:
            if user_id not in self.user_connections:
                self.user_connections[user_id] = []
            self.user_connections[user_id].append(websocket)

    def disconnect(self, websocket: WebSocket, user_id: str = None):
        self.active_connections.remove(websocket)

        # Remove from user-specific connections if user_id is provided
        if user_id and user_id in self.user_connections:
            if websocket in self.user_connections[user_id]:
                self.user_connections[user_id].remove(websocket)
                # Clean up empty lists
                if not self.user_connections[user_id]:
                    del self.user_connections[user_id]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                # If sending fails, mark for disconnection
                disconnected.append(connection)

        # Remove disconnected connections
        for connection in disconnected:
            self.active_connections.remove(connection)

    async def send_to_user(self, user_id: str, message: str):
        """Send a message to all connections of a specific user"""
        if user_id in self.user_connections:
            disconnected = []
            for connection in self.user_connections[user_id]:
                try:
                    await connection.send_text(message)
                except:
                    # If sending fails, mark for disconnection
                    disconnected.append(connection)

            # Remove disconnected connections from user's list
            for connection in disconnected:
                self.user_connections[user_id].remove(connection)
                self.active_connections.remove(connection)

                # Clean up empty lists
                if not self.user_connections[user_id]:
                    del self.user_connections[user_id]


manager = ConnectionManager()

app = FastAPI(title="WebSocket Service")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Extract user_id from query parameters or headers if available
    user_id = websocket.query_params.get("user_id")  # Expected format: ws://host:port/ws?user_id=abc123
    await manager.connect(websocket, user_id)

    try:
        # Listen for messages from client (optional, for ping/pong or acknowledgments)
        while True:
            try:
                data = await websocket.receive_text()
                # Handle client messages if needed
                logger.info(f"Received message from client: {data}")
            except WebSocketDisconnect:
                break
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)

def kafka_consumer_thread():
    """Run Kafka consumer in a separate thread"""
    # Use environment variable for Kafka broker, default to internal Docker service name
    kafka_broker = os.getenv("KAFKA_BROKER", "kafka:9092")

    consumer = KafkaConsumer(
        'task-events',  # Using the correct topic name
        bootstrap_servers=[kafka_broker],
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        group_id='websocket-group'
    )

    logger.info("Starting Kafka consumer for WebSocket service...")

    for message in consumer:
        task_event = message.value
        logger.info(f"Received task event: {task_event}")

        # Create a new event loop for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            # Broadcast the update to all connected clients
            loop.run_until_complete(manager.broadcast(json.dumps(task_event)))
        except Exception as e:
            logger.error(f"Error broadcasting task event: {e}")
        finally:
            loop.close()

def notification_kafka_consumer_thread():
    """Run Kafka consumer for notifications in a separate thread"""
    # Use environment variable for Kafka broker, default to internal Docker service name
    kafka_broker = os.getenv("KAFKA_BROKER", "kafka:9092")

    consumer = KafkaConsumer(
        'notifications',  # Using the notifications topic
        bootstrap_servers=[kafka_broker],
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        group_id='websocket-notification-group'
    )

    logger.info("Starting Kafka consumer for notification WebSocket service...")

    for message in consumer:
        notification = message.value
        logger.info(f"Received notification: {notification}")

        # Send notification to specific user if user_id is provided
        user_id = notification.get('user_id')
        if user_id:
            # Create a new event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                loop.run_until_complete(manager.send_to_user(user_id, json.dumps(notification)))
            except Exception as e:
                logger.error(f"Error sending notification to user {user_id}: {e}")
            finally:
                loop.close()
        else:
            # Broadcast to all if no specific user
            # Create a new event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                loop.run_until_complete(manager.broadcast(json.dumps(notification)))
            except Exception as e:
                logger.error(f"Error broadcasting notification: {e}")
            finally:
                loop.close()

# Global variable to hold the event loop
loop = None

@app.on_event("startup")
def startup_event():
    global loop
    loop = asyncio.get_event_loop()

    # Start Kafka consumer for task events in a separate thread
    task_consumer_thread = threading.Thread(target=kafka_consumer_thread, daemon=True)
    task_consumer_thread.start()

    # Start Kafka consumer for notifications in a separate thread
    notification_consumer_thread = threading.Thread(target=notification_kafka_consumer_thread, daemon=True)
    notification_consumer_thread.start()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)