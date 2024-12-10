import math
import os
import motor
from motor import motor_asyncio
from dotenv import load_dotenv
#from schemas.SCHEMA import *

"""
CTRL-F A CAMBIAR:
    - NOMBRE_COLLECTION
    - SCHEMA
    - IDENTIFICADOR
"""

load_dotenv(dotenv_path='.env')

MONGO_URI = os.getenv("MONGO_URI")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
database = client.databaseExamen
NOMBRE_COLLECTION_collection = database["NOMBRE_COLLECTION"]

async def add_SCHEMA(SCHEMA):
    SCHEMA_data = SCHEMA.model_dump()
    item = await NOMBRE_COLLECTION_collection.insert_one(SCHEMA_data)
    return True

async def update_SCHEMA(IDENTIFICADOR: int, SCHEMA):
    if not SCHEMA:
        return False
    item = await NOMBRE_COLLECTION_collection.find_one({"IDENTIFICADOR": IDENTIFICADOR})
    if item:
        updatedItem = await NOMBRE_COLLECTION_collection.update_one(
            {"IDENTIFICADOR": IDENTIFICADOR}, {"$set": SCHEMA}
        )
        return bool(updatedItem)
    else:
        return False

async def delete_SCHEMA(IDENTIFICADOR: int):
    deleted = False
    item = await NOMBRE_COLLECTION_collection.find_one({"IDENTIFICADOR": IDENTIFICADOR})
    if item:
        await NOMBRE_COLLECTION_collection.delete_one({"IDENTIFICADOR": IDENTIFICADOR})
        deleted = True
    return deleted


async def get_SCHEMA(filter):
    results = []
    if len(filter) > 0:
        cursor = NOMBRE_COLLECTION_collection.find(filter)
        async for document in cursor:
            document['_id'] = str(document['_id'])  # Convertir ObjectId a string
            results.append(document)
    else:
        async for item in NOMBRE_COLLECTION_collection.find():
            item["_id"] = str(item["_id"])
            results.append(item)
    return results

async def get_SCHEMA_IDENTIFICADOR(IDENTIFICADOR: int) -> dict:
    item = await NOMBRE_COLLECTION_collection.find_one({"IDENTIFICADOR": IDENTIFICADOR})
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