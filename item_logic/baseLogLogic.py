import os
import motor
from bson import ObjectId
from motor import motor_asyncio
from dotenv import load_dotenv
from schemas.baseLog import BaseLog

"""
CTRL-F A CAMBIAR:
    - NOMBRE_COLLECTION = logs
    - SCHEMA = baseLog
    - IDENTIFICADOR = id
"""

load_dotenv(dotenv_path='.env')

MONGO_URI = os.getenv("MONGO_URI")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
database = client.databaseExamen
logs_collection = database["logs"]

async def add_baseLog(baseLog: BaseLog):
    baseLog_data = baseLog.model_dump()
    item = await logs_collection.insert_one(baseLog_data)
    return True

async def update_baseLog(id: str, baseLog: BaseLog):
    if not baseLog:
        return False
    item = await logs_collection.find_one({"_id": ObjectId(id)})
    if item:
        updatedItem = await logs_collection.update_one(
            {"id": id}, {"$set": baseLog}
        )
        return bool(updatedItem)
    else:
        return False

async def delete_baseLog(id: str):
    deleted = False
    item = await logs_collection.find_one({"_id": ObjectId(id)})
    if item:
        await logs_collection.delete_one({"_id": ObjectId(id)})
        deleted = True
    return deleted


async def get_baseLog(filter):
    results = []
    if len(filter) > 0:
        cursor = logs_collection.find(filter)
        async for document in cursor:
            document['_id'] = str(document['_id'])  # Convertir ObjectId a string
            results.append(document)
    else:
        async for item in logs_collection.find():
            item["_id"] = str(item["_id"])
            results.append(item)
    return results

async def get_baseLog_id(id: str) -> dict:
    item = await logs_collection.find_one({"_id": ObjectId(id)})
    if item:
        item["_id"] = str(item["_id"])
        return item

def extract_timestamp(log):
    try:
        fullDate = str(log['timestamp'])
        dateSplitBase = fullDate.split(' ')
        yearMonthDay = dateSplitBase[0].split('-')
        dateSplitRest = dateSplitBase[1].split('.')
        hourMinuteSecond = dateSplitRest[0].split(':')

        # Crear el valor único cronológicamente ordenado
        unique_value = (
            f"{int(yearMonthDay[0]):04}"  # Año (4 dígitos)
            f"{int(yearMonthDay[1]):02}"  # Mes (2 dígitos)
            f"{int(yearMonthDay[2]):02}"  # Día (2 dígitos)
            f"{int(hourMinuteSecond[0]):02}"  # Hora (2 dígitos)
            f"{int(hourMinuteSecond[1]):02}"  # Minuto (2 dígitos)
            f"{int(hourMinuteSecond[2]):02}"  # Segundo (2 dígitos)
        )

        return int(unique_value)  # Convertir a entero para mantener orden cronológico
    except KeyError:
        return 0