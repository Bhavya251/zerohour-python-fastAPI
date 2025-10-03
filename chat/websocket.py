from fastapi import Request, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json
import asyncio
from database import get_db
from chat.models import Message
from bson import ObjectId
from typing import Dict


class ConnectionManager:
    def __init__(self):
        self.message_queues: Dict[str, asyncio.Queue] = {}

    async def connect(self, user_id: str) -> asyncio.Queue:
        """Create a message queue for the user"""
        if user_id not in self.message_queues:
            self.message_queues[user_id] = asyncio.Queue()
        return self.message_queues[user_id]

    def disconnect(self, user_id: str):
        """Remove user's message queue"""
        self.message_queues.pop(user_id, None)

    async def send_message_to_chat(self, message: dict, chat_id: str):
        """Send message to all participants in a chat"""
        db = await get_db()
        chat = await db.chats.find_one({"chat_id": chat_id})
        if chat:
            for participant_id in chat.get("participants", []):
                queue = self.message_queues.get(participant_id)
                if queue:
                    try:
                        await queue.put(message)
                    except Exception as e:
                        print(f"Error sending message to {participant_id}: {e}")

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


async def sse_endpoint(request: Request, user_id: str):
    """
    SSE endpoint for receiving real-time messages
    Usage: GET /sse/{user_id}
    """
    db = await get_db()

    # Update user online status
    await db.users.update_one(
        {"user_id": user_id},
        {"$set": {"is_online": True}}
    )

    async def event_generator():
        queue = await manager.connect(user_id)
        try:
            # Send initial connection message
            yield f"data: {json.dumps({'type': 'connected', 'user_id': user_id})}\n\n"

            while True:
                # Check if client disconnected
                if await request.is_disconnected():
                    break

                try:
                    # Wait for messages with timeout to allow checking disconnect
                    message = await asyncio.wait_for(queue.get(), timeout=30.0)
                    serialized_message = manager._serialize(message)
                    yield f"data: {json.dumps(serialized_message)}\n\n"
                except asyncio.TimeoutError:
                    # Send keepalive ping every 30 seconds
                    yield f": keepalive\n\n"

        except Exception as e:
            print(f"SSE Error for user {user_id}: {e}")
        finally:
            # Cleanup on disconnect
            manager.disconnect(user_id)
            await db.users.update_one(
                {"user_id": user_id},
                {"$set": {"is_online": False}}
            )

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # Disable buffering for nginx
        }
    )


# Pydantic model for sending messages
class SendMessageRequest(BaseModel):
    chat_id: str
    content: str


async def send_message_endpoint(user_id: str, message_request: SendMessageRequest):
    """
    REST endpoint for sending messages
    Usage: POST /send/{user_id}
    Body: {"chat_id": "...", "content": "..."}
    """
    db = await get_db()

    # Verify user has access to chat
    chat = await db.chats.find_one({"chat_id": message_request.chat_id})
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    if user_id not in chat.get("participants", []):
        raise HTTPException(status_code=403, detail="User not in chat")

    # Create Message Pydantic model
    message = Message(
        chat_id=message_request.chat_id,
        sender_id=user_id,
        content=message_request.content
    )

    await db.messages.insert_one(message.model_dump())

    # Update chat's last message
    await db.chats.update_one(
        {"chat_id": message_request.chat_id},
        {
            "$set": {
                "last_message": message_request.content,
                "last_message_time": message.timestamp
            }
        }
    )

    # Prepare broadcast message
    sender_doc = await db.users.find_one({"user_id": user_id})
    if sender_doc:
        sender_doc.pop("password_hash", None)  # remove sensitive info

    broadcast = {
        "type": "message",
        "message_id": str(message.message_id),
        "chat_id": message.chat_id,
        "content": message.content,
        "timestamp": message.timestamp.isoformat(),
        "sender": manager._serialize(sender_doc) if sender_doc else None
    }

    # Broadcast to all participants
    await manager.send_message_to_chat(broadcast, message.chat_id)

    return {
        "status": "success",
        "message_id": str(message.message_id),
        "timestamp": message.timestamp.isoformat()
    }
