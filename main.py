import json
from fastapi import FastAPI
from routers import baseLogRouter, eventoRouterTEST
from fastapi.middleware.cors import CORSMiddleware
urls = json.load(open('urls.json'))

"""
CTRL-F A CAMBIAR:
    - ROUTER
    - SCHEMA_URL
"""

"""
For requirements do:
    - pip freeze > requirements.txt
"""

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(baseLogRouter.router,prefix=urls["log_url"])

app.include_router(eventoRouterTEST.router,prefix=urls["eventTEST_url"])