from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from collections import defaultdict
import json

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.topics = defaultdict(list)

    async def connect(self, websocket: WebSocket, topic: str):
        await websocket.accept()
        self.topics[topic].append(websocket)

    def disconnect(self, websocket: WebSocket, topic: str):
        if websocket in self.topics.get(topic, []):
            self.topics[topic].remove(websocket)

    async def broadcast(self, topic: str, message: dict):
        living = []
        for ws in self.topics.get(topic, []):
            try:
                await ws.send_json(message)
                living.append(ws)
            except:
                # dead websocket
                pass
        self.topics[topic] = living

manager = ConnectionManager()

@router.websocket("/box/{topic}")
async def status_websocket(websocket: WebSocket, topic: str):
    await manager.connect(websocket, topic)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                payload  = json.loads(data)
                # TODO: add functionality on message receive HERE
            except json.JSONDecodeError:
                print('error parsing JSON')

    except WebSocketDisconnect:
        manager.disconnect(websocket, topic)