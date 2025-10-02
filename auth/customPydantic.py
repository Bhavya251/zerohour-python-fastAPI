from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from datetime import datetime
from typing import Any

# Custom ObjectId type
class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source: Any, handler):
        from pydantic_core import core_schema

        return core_schema.no_info_plain_validator_function(cls.validate)

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        """Pydantic v2 way of modifying schema."""
        schema = handler(core_schema)
        schema.update(type="string")
        return schema


# User output model
class UserOut(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: str
    first_name: str
    last_name: str
    mobile_no: str
    email: EmailStr
    username: str
    created_at: datetime
    is_online: bool = False

    model_config = dict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )
