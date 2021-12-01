from bson.objectid import ObjectId
from pydantic import BaseModel, Field, validator
from .objectid_model import PyObjectId

def check_title_not_empty(value: str) -> str:
    assert value != "", 'Empty strings are not allowed'
    return value

class PlaceBase(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    titulo: str = Field(...)
    descripcion: str = Field(...)
    horario: str = Field(...)
    imagen: str = Field(...)
    direccion: str = Field(...)
    telefono: int = Field(...)
    pagina: str = Field(...)
    tipo: str = Field(...)
    latitud: float = Field(...)
    longitud: float = Field(...)

    validar_titulo = validator('titulo', allow_reuse=True)(check_title_not_empty)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "titulo" : "Museo de la Revolución",
                "descripcion": "Museo donde se muestran artículos del centauro del norte",
                "horario" : "Lunes a viernes 9:00 a 16:00",
                "imagen" : "https://panchovilla.com",
                "direccion" : "Calle 10 3010, col Santa Rosa",
                "telefono" : 61429329323,
                "pagina" : "https://panchovilla.com",
                "tipo" : "museo",
                "latitud" : 47.359423,
                "longitud" :  -122.021071
            }
        }
