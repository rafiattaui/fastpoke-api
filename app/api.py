from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.endpoints import router
from app.httpxclient import HTTPXClient
from app.cache import RedisClient

API_URL = "https://pokeapi.co/api/v2/"

@asynccontextmanager
async def lifespan(app: FastAPI):
    await HTTPXClient.init(API_URL)
    await RedisClient.init()

    yield
    
    await HTTPXClient.close_conn()
    await RedisClient.close_conn(flush=True)

app = FastAPI(title="PokeCache API", lifespan=lifespan)
app.include_router(router)