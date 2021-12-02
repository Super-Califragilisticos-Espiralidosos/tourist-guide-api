from typing import Optional
from bson.objectid import ObjectId
from pydantic import BaseModel, EmailStr, Field, validator
from pydantic.types import Optional
from .objectid_model import PyObjectId


def password_strength_check(value: str) -> str:
    assert len(value) >= 8, 'Password must be 8 characters or longer'
    return value

def check_name_not_empty(value: str) -> str:
    assert value != "", 'Empty strings are not allowed'
    return value

class UserBase(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    email: EmailStr = Field(...)
    disabled: Optional[bool] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "email": "tim@apple.com",
                "disabled": False
            }
        }

class UserLogin(UserBase):
    password: str = Field(...)
    pwd_validate = validator('password', allow_reuse=True)(password_strength_check)

    class Config:
        schema_extra = {
            "example": {
                "email": "tim@apple.com",
                "password": "MyPwd123."
            }
        }

class UserCreate(UserBase):
    username: str = Field(...)
    password: str = Field(...)
    usr_validate = validator('username', allow_reuse=True)(check_name_not_empty)
    pwd_validate = validator('password', allow_reuse=True)(password_strength_check)
    class Config:
        schema_extra = {
            "example": {
                "username": "Tim Cook",
                "email": "tim@apple.com",
                "password": "SecretPwd1."
            }
        }
    
class UserUpdate(UserBase):
    username: Optional[str] = None
    password: Optional[str] = None
    
    @validator('username', 'password')
    def check_one_not_empty(cls, v, values, **kwargs):
        usr = 'username' in values
        pwd = 'password' in values
        if usr == "" and len(pwd) < 8:
            raise ValueError('At least one field needs to be updated')
        return values

    class Config:
        schema_extra = {
            "example": {
                "username": "Tim Cook",
                "password": "MyPwd123."
            }
        }

class UserInDB(UserBase):
    username: str = Field(...)
    hashed_password: str = Field(...)
    usr_validate = validator('username', allow_reuse=True)(check_name_not_empty)


class UserCredentials(BaseModel):
    token: str = Field(...)
    new_password: str = Field(...)
    pwd_validate = validator('new_password', allow_reuse=True)(password_strength_check)
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "token": "654nfsiotre95043jkl",
                "new_password": "ChangedPwd9."
            }
        }
