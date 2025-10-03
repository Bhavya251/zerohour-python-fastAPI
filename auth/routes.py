from fastapi import APIRouter, HTTPException, Depends
from auth.customPydantic import UserOut
from datetime import timedelta
from database import get_db
from config import ACCESS_TOKEN_EXPIRE_MINUTES
from auth.models import UserRegister, UserLogin, Token, User
from auth.utils import get_password_hash, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.post("/register", response_model=Token)
async def register_user(user_data: UserRegister):
    db = get_db()
    existing_user = await db.users.find_one({
        "$or": [{"username": user_data.username}, {"email": user_data.email}]
    })
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")

    hashed_password = get_password_hash(user_data.password)

    user_dict = user_data.model_dump()
    user_dict.pop("password")
    user = User(**user_dict)
    user_db = user.model_dump()
    user_db["password_hash"] = hashed_password
    await db.users.insert_one(user_db)

    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer", "user_data": user.model_dump()}

@router.post("/login", response_model=Token)
async def login_user(credentials: UserLogin):
    db = get_db()
    user = await db.users.find_one({"username": credentials.username})
    if not user or not verify_password(credentials.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    await db.users.update_one({"user_id": user["user_id"]}, {"$set": {"is_online": True}})

    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_data": UserOut(**user)   # 👈 properly serialized
    }

@router.post("/logout")
async def logout_user(current_user: UserOut = Depends(get_current_user)):
    db = get_db()
    await db.users.update_one({"user_id": current_user.user_id}, {"$set": {"is_online": False}})
    return {"message": "Successfully logged out"}
