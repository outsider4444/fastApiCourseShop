from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from db import database
from resources.routes import api_router


origin = [
    "http://localhost:8000",
    "http://127.0.0.1",
]


app = FastAPI()
app.include_router(api_router)
app.add_middleware(
    CORSMiddleware,
    allow_origin=True,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")  # Подключение к базе данных
async def startup():
    await database.connect()


@app.on_event("shutdown")  # Отключение от базы данных
async def shutdown():
    await database.disconnect()
