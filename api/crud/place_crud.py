from typing import Optional, List
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from ..models import place_model
from ..core import settings

list_limit = 1000

class CRUDPlace():
    async def create(request: Request, obj_in: place_model.PlaceBase) -> Optional[place_model.PlaceBase]:
        new_place = place_model.PlaceBase(
            titulo=obj_in['titulo'],
            descripcion=obj_in['descripcion'],
            horario=obj_in['horario'],
            imagen=obj_in['imagen'],
            direccion=obj_in['direccion'],
            telefono=obj_in['telefono'],
            pagina=obj_in['pagina'],
            tipo=obj_in['tipo'],
            latitud=obj_in['latitud'],
            longitud=obj_in['longitud']
        )
        serialized_place = jsonable_encoder(new_place)
        new_place= await request.app.mongodb[settings.MONGODB_COLLECTION_PLACES].insert_one(serialized_place)
        return serialized_place

    async def get_places(request: Request) -> Optional[List[place_model.PlaceBase]]:
        places = await request.app.mongodb[settings.MONGODB_COLLECTION_PLACES].find().to_list(list_limit)
        return places

    async def get_place_by_id(request: Request, id: str) -> Optional[place_model.PlaceBase]:
        if (place := await request.app.mongodb[settings.MONGODB_COLLECTION_PLACES].find_one({"_id": id})) is not None:
            return place
        else: return None
