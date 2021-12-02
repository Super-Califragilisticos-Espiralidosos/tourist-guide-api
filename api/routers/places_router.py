from fastapi import APIRouter, Request, status, Path
from fastapi.encoders import jsonable_encoder
from fastapi.param_functions import Depends
from fastapi.responses import JSONResponse
from ..models import place_model, user_model
from ..services.place_service import PlaceService
from ..services.user_service import UserService
from typing import List

router = APIRouter(
    prefix="/places",
    tags=["places"],
    responses={404: {"description" : "Not found"}}
)

@router.post("/new", status_code=status.HTTP_201_CREATED, response_description="Create new place", response_model=place_model.PlaceBase)
async def create_place(request: Request, place_in: place_model.PlaceBase, current_user: user_model.UserInDB = Depends(UserService.get_current_active_user)) -> JSONResponse:
    place_in = jsonable_encoder(place_in)
    new_place = await PlaceService.create(request, place_in)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        "message" : "Place added successfully",
        "user" : current_user['_id'],
        "data" : new_place
        }
    )

@router.get("/list", status_code=status.HTTP_200_OK, response_description="List all places", response_model=List[place_model.PlaceBase])
async def get_all_places(request: Request, current_user: user_model.UserInDB = Depends(UserService.get_current_active_user)) -> JSONResponse:
    places_information = await PlaceService.get_all_places(request)
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        "message" : "List retrieved successfully",
        "user" : current_user['_id'],
        "data": places_information
        }
    )

@router.get("/{id}", status_code=status.HTTP_200_OK, response_description="Attraction Information", response_model=place_model.PlaceBase)
async def get_place(request: Request, id: str = Path(..., title="The ID of the place to get"), current_user: user_model.UserInDB = Depends(UserService.get_current_active_user)) -> JSONResponse:
    place_information = await PlaceService.get_place_by_id(request, id)
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        "message" : "Place retrieved successfully",
        "user" : current_user['_id'],
        "data": place_information
        }
    )
