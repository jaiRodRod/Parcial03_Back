from datetime import datetime, timezone, timedelta
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator, field_serializer


class BaseLog(BaseModel):

    timestamp: datetime = Field(...)
    email: str = Field(min_length=1)
    usuario_visitado: str = Field(min_length=1)
    token: str = Field(min_length=1)

    model_config = {
        "json_schema_extra": {
            "example": {
                "timestamp": "2014-12-31T10:30:00.000",
                "email": "juan@uma.es",
                "usuario_visitado": "jaezro03@gmail.com",
                "token": "1289dqwu1892d10j",
            }
        }
    }


    #@field_serializer("date", mode="plain")
    #def serialize_date(slogelf, value: datetime) -> str:
        #return value.isoformat()