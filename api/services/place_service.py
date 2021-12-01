from fastapi import Request, HTTPException, status
from typing import Optional, List
from ..crud.place_crud import CRUDPlace
from ..models import place_model

class PlaceService():
    async def create(request: Request, place_in: place_model.PlaceBase) -> Optional[place_model.PlaceBase]:
        place = await CRUDPlace.create(request, place_in)
        if not place:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Place could not be created"
            )
        return place
    
    async def get_all_places(request: Request) -> Optional[List[place_model.PlaceBase]]:
        retrieved_places = await CRUDPlace.get_places(request)
        if not retrieved_places:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Places not found"
            )
        return retrieved_places

    async def get_place_by_id(request: Request, id: str) -> Optional[place_model.PlaceBase]:
        retrieved_place = await CRUDPlace.get_place_by_id(request, id)
        if not retrieved_place:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Place with ID {id} not found"
            )
        return retrieved_place
