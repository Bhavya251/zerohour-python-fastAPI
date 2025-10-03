from fastapi import APIRouter, Depends
from database import get_db
from auth.models import User
from auth.utils import get_current_user


router = APIRouter(prefix="/api/users", tags=["Users"])

# User endpoints
@router.get("/search")
async def search_users(query: str, current_user: User = Depends(get_current_user)):
    db = await get_db()
    users = await db.users.find({
        "$and": [
            {"user_id": {"$ne": current_user.user_id}},
            {"$or": [
                {"username": {"$regex": query, "$options": "i"}},
                {"first_name": {"$regex": query, "$options": "i"}},
                {"last_name": {"$regex": query, "$options": "i"}}
            ]}
        ]
    }).to_list(20)

    return [
        {
            "user_id": user["user_id"],
            "username": user["username"],
            "first_name": user["first_name"],
            "last_name": user["last_name"],
            "is_online": user.get("is_online", False)
        } for user in users
    ]

