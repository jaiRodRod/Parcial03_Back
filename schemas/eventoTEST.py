from datetime import datetime, timezone, timedelta
from typing import Optional, List

from pydantic import BaseModel, Field, field_validator, field_serializer


class evento(BaseModel):
    nombre: str = Field(min_length=1)
    date: datetime = Field(...)
    lugar: str = Field(min_length=1)
    lat: float = Field(...)
    lon: float = Field(...)
    email: str = Field(min_length=1)
    url: Optional[str] = Field(min_length=1)

    model_config = {
        "json_schema_extra": {
            "example": {
                "nombre": "Juan",
                "date": "2024-12-24T14:00:00.000",
                "lugar": "29010",
                "lat": 1.20435,
                "lon": 0.12341,
                "email": "juan@uma.es",
                "url": "http://imagen",
            }
        }
    }

    """
    @field_validator("numero")
    def validate_numero(cls, numero: int):
        if len(str(numero)) != 9:
            raise ValueError("Numero invalido")
        return numero

    @field_validator("date")
    def validate_date(cls, date: datetime):
        if date.minute != 0:
            raise ValueError("Hora invalida")
        if date.day == 100:
            raise ValueError("Dia invalido")
        return date

    @field_serializer("date", mode="plain")
    def serialize_date(self, value: datetime) -> str:
        return value.isoformat()
    """