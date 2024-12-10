import math
from http.client import HTTPException
from typing import Optional

from fastapi import APIRouter, Body
from fastapi.params import Query
from pymongo.errors import DuplicateKeyError

from item_logic.baseItemLogic import haversine
import item_logic.eventoItemLogicTEST as eventoItemLogicTEST
from schemas.eventoTEST import evento as eventoTEST

router = APIRouter()

"""
CTRL-F A CAMBIAR:
    - NOMBRE_LOGIC = eventoItemLogicTEST
    - SCHEMA = eventoTEST
    - IDENTIFICADOR = id
"""

@router.post("/")
async def add_eventoTEST(eventoTEST: eventoTEST = Body(...)):
    try:
        #exists = await eventoItemLogicTEST.get_eventoTEST_id(eventoTEST._id)
        #if not exists:
            result = await eventoItemLogicTEST.add_eventoTEST(eventoTEST)
            return result
        #else:
        #    raise HTTPException(status_code=500,detail="Usuario ya existente")

    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Email already exists")


@router.get("/")
async def get_eventoTEST(
        #filter_str: Optional[str] = Query(None),
        #sort_by_newest: Optional[bool] = Query(None),
        lugar: Optional[str] = None,
        latitude: Optional[float] = Query(None),
        longitude: Optional[float] = Query(None),
        #radius: Optional[float] = Query(None),
):
    filter = {}
    """
    if filter_str:
        filter["str"] = filter_str
    """
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

    if latitude and longitude:
        delta = 0.2
        lat_min = latitude - delta
        lat_max = latitude + delta
        lon_min = longitude - delta
        lon_max = longitude + delta

        filter.update({
            "lat": {"$gte": lat_min, "$lte": lat_max},
            "lon": {"$gte": lon_min, "$lte": lon_max},
        })

    if lugar:
        filter["lugar"] = lugar

    items = await eventoItemLogicTEST.get_eventoTEST(filter)

    """
    if latitude and longitude and radius:
        items = [
            place for place in items
            if haversine(place['lat'], place['lon'], latitude, longitude) <= radius
        ]
    """

    #if sort_by_newest
    items.sort(key=eventoItemLogicTEST.extract_date, reverse=True)

    return items

@router.get("/{id}")
async def get_eventoTEST_id(id: str):
    result = await eventoItemLogicTEST.get_eventoTEST_id(id)
    if result:
        result["_id"] = str(result["_id"])
        return result
    raise HTTPException(status_code=500, details="Usuario no encontrado")

@router.delete("/{id}")
async def delete_eventoTEST(id: str):
    result = await eventoItemLogicTEST.delete_eventoTEST(id)
    return result

@router.patch("/{id}")
async def update_user(id: str, req: eventoTEST = Body(...)):
    req = {k: v for k, v in req.model_dump().items() if v is not None}
    result = await eventoItemLogicTEST.update_eventoTEST(id,req)
    return result