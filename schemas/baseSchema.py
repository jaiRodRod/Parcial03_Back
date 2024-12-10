from datetime import datetime, timezone, timedelta
from typing import Optional, List

from pydantic import BaseModel, Field, field_validator, field_serializer


class entidad(BaseModel):
    cadena: str = Field(min_length=1)
    numero: int = Field(...)
    date: datetime = Field(default_factory=lambda: datetime.now(timezone(timedelta(hours=2))))
    lat: float = Field(...)
    lon: float = Field(...)
    email: str = Field(min_length=1)
    url: Optional[str] = Field(min_length=1)
    numeroOpcional: Optional[int] = Field(None,ge=0,le=10) #La puntuacion que le da el usuario a la entrada del 0 al 10

    model_config = {
        "json_schema_extra": {
            "example": {
                "cadena": "Juan",
                "numero": 111111111,
                "date": "2014-12-31T10:30:00.000",
                "lat": 1.20435,
                "lon": 0.12341,
                "email": "juan@uma.es",
                "url": "http://imagen",
                "numeroOpcional": 1,
            }
        }
    }

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