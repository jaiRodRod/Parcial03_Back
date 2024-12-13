import math
import os
import motor
from bson import ObjectId
from motor import motor_asyncio
from dotenv import load_dotenv
from schemas.localizacionSchema import localizacion

"""
CTRL-F A CAMBIAR:
    - NOMBRE_COLLECTION = localizacion_collection
    - SCHEMA = localizacion
    - IDENTIFICADOR = id
"""

load_dotenv(dotenv_path='.env')

MONGO_URI = os.getenv("MONGO_URI")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
database = client.databaseExamen
localizacion_collection_collection = database["localizacion_collection"]

async def add_localizacion(localizacion: localizacion):
    localizacion_data = localizacion.model_dump()
    item = await localizacion_collection_collection.insert_one(localizacion_data)
    return True

async def update_localizacion(id: str, localizacion: localizacion):
    if not localizacion:
        return False
    item = await localizacion_collection_collection.find_one({"_id": ObjectId(id)})
    if item:
        updatedItem = await localizacion_collection_collection.update_one(
            {"_id": id}, {"$set": localizacion}
        )
        return bool(updatedItem)
    else:
        return False

async def delete_localizacion(id: str):
    deleted = False
    item = await localizacion_collection_collection.find_one({"_id": ObjectId(id)})
    if item:
        await localizacion_collection_collection.delete_one({"_id": ObjectId(id)})
        deleted = True
    return deleted


async def get_localizacion(filter):
    results = []
    if len(filter) > 0:
        cursor = localizacion_collection_collection.find(filter)
        async for document in cursor:
            document['_id'] = str(document['_id'])  # Convertir ObjectId a string
            results.append(document)
    else:
        async for item in localizacion_collection_collection.find():
            item["_id"] = str(item["_id"])
            results.append(item)
    return results

async def get_localizacion_id(id: str) -> dict:
    item = await localizacion_collection_collection.find_one({"_id": ObjectId(id)})
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