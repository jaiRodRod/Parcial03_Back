from datetime import datetime, timezone, timedelta
from typing import Optional, List

from pydantic import BaseModel, Field, field_validator, field_serializer


class localizacion(BaseModel):
    nombre: str = Field(min_length=1)
    lugar: str = Field(min_length=1)
    lat: float = Field(...)
    lon: float = Field(...)
    email: str = Field(min_length=1)
    url: Optional[str] = Field(min_length=1)

    model_config = {
        "json_schema_extra": {
            "example": {
                "nombre": "Juan",
                "lugar": "29010",
                "lat": 1.20435,
                "lon": 0.12341,
                "email": "juan@uma.es",
                "url": "http://imagen",
            }
        }
    }