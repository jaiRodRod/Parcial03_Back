import math
import os
import motor
from bson import ObjectId
from motor import motor_asyncio
from dotenv import load_dotenv
from schemas.eventoTEST import evento as eventoTEST

"""
CTRL-F A CAMBIAR:
    - NOMBRE_COLLECTION = eventos
    - SCHEMA = eventoTEST
    - IDENTIFICADOR = id
"""

load_dotenv(dotenv_path='.env')

MONGO_URI = os.getenv("MONGO_URI")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
database = client.databaseExamen
eventos_collection = database["eventos"]

async def add_eventoTEST(eventoTEST: eventoTEST):
    eventoTEST_data = eventoTEST.model_dump()
    item = await eventos_collection.insert_one(eventoTEST_data)
    return True

async def update_eventoTEST(id: str, eventoTEST: eventoTEST):
    if not eventoTEST:
        return False
    item = await eventos_collection.find_one({"_id": ObjectId(id)})
    if item:
        updatedItem = await eventos_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": eventoTEST}
        )
        return bool(updatedItem)
    else:
        return False

async def delete_eventoTEST(id: str):
    deleted = False
    item = await eventos_collection.find_one({"_id": ObjectId(id)})
    if item:
        await eventos_collection.delete_one({"_id": ObjectId(id)})
        deleted = True
    return deleted


async def get_eventoTEST(filter):
    results = []
    if len(filter) > 0:
        cursor = eventos_collection.find(filter)
        async for document in cursor:
            document['_id'] = str(document['_id'])  # Convertir ObjectId a string
            results.append(document)
    else:
        async for item in eventos_collection.find():
            item["_id"] = str(item["_id"])
            results.append(item)
    return results

async def get_eventoTEST_id(id: str) -> dict:
    item = await eventos_collection.find_one({"_id": ObjectId(id)})
    if item:
        item["_id"] = str(item["_id"])
        return item

def extract_date(commentary):
    try:
        fullDate = str(commentary['date'])
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

def haversine(lat_device, lon_device, lat, lon):
    R = 6371000  # Radio de la Tierra en metros
    phi1 = math.radians(lat_device)
    phi2 = math.radians(lat)
    delta_phi = math.radians(lat - lat_device)
    delta_lambda = math.radians(lon - lon_device)

    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c  # Resultado en metros