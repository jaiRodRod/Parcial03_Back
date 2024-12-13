import math
from http.client import HTTPException
from typing import Optional

from fastapi import APIRouter, Body
from fastapi.params import Query
from pymongo.errors import DuplicateKeyError

from item_logic.localizacionItemLogic import haversine
import item_logic.localizacionItemLogic as localizacion_logic
from schemas.localizacionSchema import localizacion

router = APIRouter()

"""
CTRL-F A CAMBIAR:
    - NOMBRE_LOGIC = localizacion_logic
    - SCHEMA = localizacion
    - IDENTIFICADOR = id
"""

@router.post("/")
async def add_localizacion(localizacion: localizacion = Body(...)):
    try:
        result = await localizacion_logic.add_localizacion(localizacion)
        return result
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Email already exists")


@router.get("/")
async def get_localizacion(
        #filter_str: Optional[str] = Query(None),
        #sort_by_newest: Optional[bool] = Query(None),
        #latitude: Optional[float] = Query(None),
        #longitude: Optional[float] = Query(None),
        #radius: Optional[float] = Query(None),
        user_email: Optional[str] = Query(None),
):
    filter = {}

    if user_email:
        filter["email"] = user_email
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
    """


    items = await localizacion_logic.get_localizacion(filter)

    """
    if sort_by_newest:
        items.sort(key=localizacion_logic.extract_date, reverse=True)

    if latitude and longitude and radius:
        items = [
            place for place in items
            if haversine(place['lat'], place['lon'], latitude, longitude) <= radius
        ]
    """

    return items

@router.get("/{id}")
async def get_localizacion_id(id: str):
    result = await localizacion_logic.get_localizacion_id(id)
    if result:
        result["_id"] = str(result["_id"])
        return result
    raise HTTPException(status_code=500, details="Usuario no encontrado")

@router.delete("/{id}")
async def delete_localizacion(id: str):
    result = await localizacion_logic.delete_localizacion(id)
    return result

@router.patch("/{id}")
async def update_user(id: str, req: localizacion = Body(...)):
    req = {k: v for k, v in req.model_dump().items() if v is not None}
    result = await localizacion_logic.update_localizacion(id,req)
    return result