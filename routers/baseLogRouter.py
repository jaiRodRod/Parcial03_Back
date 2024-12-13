from http.client import HTTPException
from typing import Optional

from fastapi import APIRouter, Body, Query
from pymongo.errors import DuplicateKeyError

import item_logic.baseLogLogic as logs
from schemas.baseLog import BaseLog

router = APIRouter()

"""
CTRL-F A CAMBIAR:
    - NOMBRE_LOGIC = logs
    - SCHEMA = baseLog
    - IDENTIFICADOR = id
"""

@router.post("/")
async def add_baseLog(baseLog: BaseLog = Body(...)):
    try:
        result = await logs.add_baseLog(baseLog)
        return result
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Email already exists")


@router.get("/")
async def get_baseLog(
        usuario_visitado: Optional[str] = Query(None),
        sort: Optional[bool] = Query(None),
):
    filter = {}
    if usuario_visitado:
        filter["usuario_visitado"] = usuario_visitado

    items = await logs.get_baseLog(filter)

    if sort:
        items.sort(key=logs.extract_timestamp, reverse=True)

    return items

@router.get("/{id}")
async def get_baseLog_id(id: str):
    result = await logs.get_baseLog_id(id)
    if result:
        result["_id"] = str(result["_id"])
        return result
    raise HTTPException(status_code=500, details="Log no encontrado")

@router.delete("/{id}")
async def delete_baseLog(id: str):
    result = await logs.delete_baseLog(id)
    return result

@router.patch("/{id}")
async def update_user(id: str, req: BaseLog = Body(...)):
    req = {k: v for k, v in req.model_dump().items() if v is not None}
    result = await logs.update_baseLog(id,req)
    return result