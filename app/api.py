from fastapi import FastAPI
from contextlib import asynccontextmanager
import httpx
from app.endpoints import router
from app.httpxclient import HTTPXClient
from app.cache import RedisClient

API_URL = "https://pokeapi.co/api/v2/"

@asynccontextmanager
async def lifespan(app: FastAPI):
    await HTTPXClient.init(API_URL)
    await RedisClient.init()

    yield

    await RedisClient.close_conn()

app = FastAPI(title="PokeCache API", lifespan=lifespan)
app.include_router(router)