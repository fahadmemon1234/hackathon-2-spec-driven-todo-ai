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

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
    
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                # If sending fails, remove the connection
                self.disconnect(connection)

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
    await manager.connect(websocket)
    try:
        while True:
            # We don't expect to receive messages from clients in this implementation
            # The WebSocket is used to broadcast updates from Kafka
            data = await websocket.receive_text()
            # In a real implementation, you might want to handle client messages
    except WebSocketDisconnect:
        manager.disconnect(websocket)

def kafka_consumer_thread():
    """Run Kafka consumer in a separate thread"""
    consumer = KafkaConsumer(
        'task-updates',
        bootstrap_servers=['my-cluster-kafka-brokers.kafka.svc.cluster.local:9092'],
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        group_id='websocket-group'
    )
    
    logger.info("Starting Kafka consumer for WebSocket service...")
    
    for message in consumer:
        task_update = message.value
        logger.info(f"Received task update: {task_update}")
        
        # Broadcast the update to all connected clients
        asyncio.run_coroutine_threadsafe(
            manager.broadcast(json.dumps(task_update)),
            loop
        )

# Start the Kafka consumer when the app starts
loop = None

@app.on_event("startup")
def startup_event():
    global loop
    loop = asyncio.get_event_loop()
    
    # Start Kafka consumer in a separate thread
    consumer_thread = threading.Thread(target=kafka_consumer_thread, daemon=True)
    consumer_thread.start()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)