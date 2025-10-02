from fastapi import APIRouter, HTTPException, Depends
from typing import List
from database import db
from auth.models import User
from chat.models import Chat
from auth.utils import get_current_user
from auth.customPydantic import UserOut

router = APIRouter(prefix="/api/chats", tags=["Chat"])

# Chat endpoints
@router.post("/create")
async def create_chat(other_user_id: str, current_user: UserOut = Depends(get_current_user)):
    # Check if chat already exists between these users
    existing_chat = await db.chats.find_one({
        "participants": {"$all": [current_user.user_id, other_user_id]}
    })

    if existing_chat:
        return Chat(**existing_chat)

    # Create new chat
    chat = Chat(participants=[current_user.user_id, other_user_id])
    await db.chats.insert_one(chat.model_dump())
    return chat


@router.get("/", response_model=List[dict])
async def get_user_chats(current_user: UserOut = Depends(get_current_user)):
    # Fetch chats where current user is a participant
    chats = await db.chats.find({
        "participants": current_user.user_id
    }).to_list(100)

    enhanced_chats = []

    for chat in chats:
        # Identify the other participant
        other_user_id = next(p for p in chat["participants"] if p != current_user.user_id)

        # Fetch other user document
        other_user_doc = await db.users.find_one({"user_id": other_user_id})
        if not other_user_doc:
            continue  # skip if user not found

        # Ensure _id exists for Pydantic model
        other_user_doc.setdefault("_id", None)
        other_user_doc.setdefault("is_online", False)

        other_user = UserOut(**other_user_doc)

        # Build enhanced chat object
        enhanced_chats.append({
            "chat_id": chat["chat_id"],
            "other_user": {
                "user_id": other_user.user_id,
                "username": other_user.username,
                "first_name": other_user.first_name,
                "last_name": other_user.last_name,
                "is_online": other_user.is_online
            },
            "last_message": chat.get("last_message"),
            "last_message_time": chat.get("last_message_time"),
            "created_at": chat["created_at"]
        })

    # Sort chats by last message time (or created_at if no messages)
    enhanced_chats.sort(
        key=lambda x: x.get("last_message_time") or x["created_at"],
        reverse=True
    )

    return enhanced_chats


@router.get("/{chat_id}/messages", response_model=List[dict])
async def get_chat_messages(chat_id: str, current_user: User = Depends(get_current_user)):
    # Verify user is participant in chat
    chat = await db.chats.find_one({"chat_id": chat_id})
    if not chat or current_user.user_id not in chat["participants"]:
        raise HTTPException(status_code=403, detail="Access denied")

    messages = await db.messages.find({"chat_id": chat_id}).sort("timestamp", 1).to_list(1000)

    # Enhance messages with sender info
    enhanced_messages = []
    for message in messages:
        sender = await db.users.find_one({"user_id": message["sender_id"]})
        enhanced_message = {
            "message_id": message["message_id"],
            "content": message["content"],
            "timestamp": message["timestamp"],
            "sender": {
                "user_id": sender["user_id"],
                "username": sender["username"],
                "first_name": sender["first_name"],
                "last_name": sender["last_name"]
            },
            "is_own_message": message["sender_id"] == current_user.user_id
        }
        enhanced_messages.append(enhanced_message)

    return enhanced_messages
