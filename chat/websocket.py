from fastapi import WebSocket, WebSocketDisconnect
import json
from database import get_db
from chat.models import Message
from bson import ObjectId

class ConnectionManager:
    # def __init__(self):
    #     self.active_connections = {}
    #
    # async def connect(self, websocket: WebSocket, user_id: str):
    #     await websocket.accept()
    #     self.active_connections[user_id] = websocket
    #
    # def disconnect(self, user_id: str):
    #     self.active_connections.pop(user_id, None)

    async def send_message_to_chat(self, message: dict, chat_id: str):
        db = await get_db()
        chat = await db.chats.find_one({"chat_id": chat_id})
        if chat:
            for participant_id in chat.get("participants", []):
                ws = self.active_connections.get(participant_id)
                if ws:
                    await ws.send_text(json.dumps(self._serialize(message)))

    def _serialize(self, obj: dict) -> dict:
        """Convert ObjectId and datetime to JSON-serializable format."""
        serialized = {}
        for k, v in obj.items():
            if isinstance(v, ObjectId):
                serialized[k] = str(v)
            elif hasattr(v, "isoformat"):  # datetime
                serialized[k] = v.isoformat()
            elif isinstance(v, dict):
                serialized[k] = self._serialize(v)
            else:
                serialized[k] = v
        return serialized

manager = ConnectionManager()

async def websocket_endpoint(websocket: WebSocket, user_id: str):
    db = await get_db()
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)

            # Create Message Pydantic model
            message = Message(
                chat_id=message_data["chat_id"],
                sender_id=user_id,
                content=message_data["content"]
            )
            await db.messages.insert_one(message.model_dump())

            # Update chat's last message
            await db.chats.update_one(
                {"chat_id": message_data["chat_id"]},
                {"$set": {"last_message": message_data["content"], "last_message_time": message.timestamp}}
            )

            # Prepare broadcast message
            sender_doc = await db.users.find_one({"user_id": user_id})
            sender_doc.pop("password_hash", None)  # remove sensitive info

            broadcast = {
                "message_id": str(message.message_id),
                "chat_id": message.chat_id,
                "content": message.content,
                "timestamp": message.timestamp.isoformat(),
                "sender": manager._serialize(sender_doc)
            }

            await manager.send_message_to_chat(broadcast, message.chat_id)

    except WebSocketDisconnect:
        manager.disconnect(user_id)
        await db.users.update_one({"user_id": user_id}, {"$set": {"is_online": False}})
