import math
from http.client import HTTPException
from typing import Optional

from fastapi import APIRouter, Body
from fastapi.params import Query
from pymongo.errors import DuplicateKeyError

from item_logic.baseItemLogic import haversine
#import item_logic.NOMBRE_LOGIC as NOMBRE_LOGIC
#from schemas.SCHEMA import *

router = APIRouter()

"""
CTRL-F A CAMBIAR:
    - NOMBRE_LOGIC
    - SCHEMA
    - IDENTIFICADOR
"""

@router.post("/")
async def add_SCHEMA(SCHEMA: SCHEMA = Body(...)):
    try:
        exists = await NOMBRE_LOGIC.get_SCHEMA_IDENTIFICADOR(SCHEMA.IDENTIFICADOR)
        if not exists:
            result = await NOMBRE_LOGIC.add_SCHEMA(SCHEMA)
            return result
        else:
            raise HTTPException(status_code=500,detail="Usuario ya existente")

    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Email already exists")


@router.get("/")
async def get_SCHEMA(
        #filter_str: Optional[str] = Query(None),
        #sort_by_newest: Optional[bool] = Query(None),
        latitude: Optional[float] = Query(None),
        longitude: Optional[float] = Query(None),
        radius: Optional[float] = Query(None),
):
    filter = {}
    """
    if filter_str:
        filter["str"] = filter_str
    """
    if latitude and longitude and radius:
        delta_lat = radius / 111000
        delta_lon = radius / (111000 * math.cos(math.radians(latitude)))
        lat_min = latitude - delta_lat
        lat_max = latitude + delta_lat
        lon_min = longitude - delta_lon
        lon_max = longitude + delta_lon

        filter.update({
            "lat": {"$gte": lat_min, "$lte": lat_max},
            "lon": {"$gte": lon_min, "$lte": lon_max},
        })


    items = await NOMBRE_LOGIC.get_SCHEMA(filter)

    """
    if sort_by_newest:
        items.sort(key=NOMBRE_LOGIC.extract_date, reverse=True)
    """

    if latitude and longitude and radius:
        items = [
            place for place in items
            if haversine(place['lat'], place['lon'], latitude, longitude) <= radius
        ]

    return items

@router.get("/{IDENTIFICADOR}")
async def get_SCHEMA_IDENTIFICADOR(IDENTIFICADOR: int):
    result = await NOMBRE_LOGIC.get_SCHEMA_IDENTIFICADOR(IDENTIFICADOR)
    if result:
        result["_id"] = str(result["_id"])
        return result
    raise HTTPException(status_code=500, details="Usuario no encontrado")

@router.delete("/{IDENTIFICADOR}")
async def delete_SCHEMA(IDENTIFICADOR: int):
    result = await NOMBRE_LOGIC.delete_SCHEMA(IDENTIFICADOR)
    return result

@router.patch("/{IDENTIFICADOR}")
async def update_user(IDENTIFICADOR: int, req: SCHEMA = Body(...)):
    req = {k: v for k, v in req.model_dump().items() if v is not None}
    result = await NOMBRE_LOGIC.update_SCHEMA(IDENTIFICADOR,req)
    return result