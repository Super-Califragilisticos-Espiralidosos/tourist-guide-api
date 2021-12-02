from fastapi import APIRouter, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.param_functions import Depends
from fastapi.responses import JSONResponse
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from api.models import token_model
from ..models import user_model
from ..services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description" : "Not found"}}
)

@router.post("/signup", status_code=status.HTTP_201_CREATED, response_description="Create new user", response_model=user_model.UserInDB)
async def create_user(request: Request, user_in: user_model.UserCreate) -> JSONResponse:
    user_in = jsonable_encoder(user_in)
    new_user = await UserService.create(request, user_in)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message" : "User added successfully", "data" : new_user})

@router.post("/token", status_code=status.HTTP_200_OK, response_description="Login with token", response_model=token_model.TokenBase)
async def login_for_access_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends()) -> JSONResponse:
    auth_user = await UserService.authenticate_user(request, form_data.username, form_data.password)
    token_data = await UserService.token_authentication(request, auth_user)
    return JSONResponse(status_code=status.HTTP_200_OK, content=token_data)

@router.get("/me", status_code=status.HTTP_200_OK, response_description="Return current user", response_model=user_model.UserInDB)
async def read_current_user(request: Request, current_user: user_model.UserInDB = Depends(UserService.get_current_active_user)) -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message" : "Current user retrieved", "data" : current_user})
