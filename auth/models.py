from pydantic import BaseModel, Field, EmailStr
from auth.customPydantic import UserOut
from datetime import datetime
import uuid

class User(BaseModel):
    user_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    first_name: str
    last_name: str
    mobile_no: str
    email: EmailStr
    username: str
    security_phrase: str
    created_at: datetime = Field(default_factory=datetime.now)
    is_online: bool = False

class UserRegister(BaseModel):
    first_name: str
    last_name: str
    mobile_no: str
    email: EmailStr
    username: str
    password: str
    security_phrase: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user_data: UserOut
