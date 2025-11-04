from fastapi import FastAPI
from contextlib import asynccontextmanager
import httpx
from app.endpoints import router
from app.dependencies import set_http_client

@asynccontextmanager
async def lifespan(app: FastAPI):
    client = httpx.AsyncClient(base_url="https://pokeapi.co/api/v2/")
    set_http_client(client)
    yield
    await client.aclose()

app = FastAPI(title="PokeCache API", lifespan=lifespan)
app.include_router(router)