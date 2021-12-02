from typing import Optional
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from ..models import user_model
from ..core.security import get_password_hash
from ..core import settings

class CRUDUser():
    async def get_by_email(request: Request, email: str) -> Optional[user_model.UserInDB]:
        if (user := await request.app.mongodb[settings.MONGODB_COLLECTION_USERS].find_one({"email": email})) is not None:
            return user
        else: return None

    async def get_by_id(request: Request, id: str) -> Optional[user_model.UserInDB]:
        if (user := await request.app.mongodb[settings.MONGODB_COLLECTION_USERS].find_one({"_id": id})) is not None:
            return user
        else: return None

    async def get_by_username(request: Request, username: str) -> Optional[user_model.UserInDB]:
        if (user := await request.app.mongodb[settings.MONGODB_COLLECTION_USERS].find_one({"username": username})) is not None:
            return user
        else: return None

    async def create(request: Request, obj_in: user_model.UserCreate) -> Optional[user_model.UserInDB]:
        new_user = user_model.UserInDB(
            email=obj_in['email'],
            username=obj_in['username'],
            hashed_password=get_password_hash(obj_in['password']),
            disabled=False
        )
        serialized_user = jsonable_encoder(new_user)
        new_user = await request.app.mongodb[settings.MONGODB_COLLECTION_USERS].insert_one(serialized_user)
        return serialized_user
