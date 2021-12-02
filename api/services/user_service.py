from datetime import timedelta
from fastapi import Request, HTTPException, Depends, status
from typing import Optional
from ..crud.user_crud import CRUDUser
from ..models import user_model, token_model
from ..core import security, settings
from jose import JWTError, jwt

class UserService():
    async def get_user_by_id(request: Request, id: str) -> Optional[user_model.UserInDB]:
        retrieved_user = await CRUDUser.get_by_id(request, id)
        if not retrieved_user:
            raise HTTPException(
                status_code=404, 
                detail=f"User with ID {id} not found"
            )
        return retrieved_user

    async def get_user_by_email(request: Request, user_in: user_model.UserBase) -> Optional[user_model.UserInDB]:
        retrieved_user = await CRUDUser.get_by_email(request, user_in)
        if not retrieved_user:
            raise HTTPException(
                status_code=404,
                detail=f"User with email {user_in['email']} not found"
            )
        return retrieved_user

    async def create(request: Request, user_in: user_model.UserCreate) -> Optional[user_model.UserInDB]:
        existing_user = await CRUDUser.get_by_email(request, user_in)
        if existing_user:
            raise HTTPException(
                status_code=409,
                detail=f"User with email {existing_user['email']} already exists in the system."
            )
        user = await CRUDUser.create(request, user_in)
        return user

    async def get_current_user(request: Request, token: str = Depends(security.oauth2_scheme)) -> Optional[user_model.UserInDB]:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise security.credentials_exception
            token_data = token_model.TokenData(email=email)
        except JWTError:
            raise security.credentials_exception
        user = await CRUDUser.get_by_email(request, token_data.email)
        if user is None:
            raise security.credentials_exception
        return user

    async def get_current_active_user(request: Request, current_user: user_model.UserInDB = Depends(get_current_user)) -> Optional[user_model.UserInDB]:
        if current_user['disabled']:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user

    async def authenticate_user(request: Request, username: str, password: str) -> Optional[user_model.UserInDB]:
        existing_user = await CRUDUser.get_by_email(request, username)
        if not existing_user:
            return False
        if not security.authenticate(password, existing_user['hashed_password']):
            return False
        return existing_user
        
    async def token_authentication(request: Request, auth_user: user_model.UserInDB):
        if not auth_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = security.create_access_token(
            data={"sub": auth_user['email']}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
