from fastapi import APIRouter, Depends, BackgroundTasks
import httpx
from app.httpxclient import HTTPXClient
from app.cache import RedisClient

API_URL = "https://pokeapi.co/api/v2/"

router = APIRouter()

@router.get("/pokemon") # /pokemon?name=Pikachu
async def get_pokemon_by_name(name: str, backgroundtask: BackgroundTasks, http: httpx.AsyncClient = Depends(HTTPXClient.get_http_client)):
    cached = await RedisClient.get_cache_by_key(f"cache:pokemon:{name}")
    if cached:
        print(f"Returning cached pokemon {name} data!", flush=True)
        return cached
    
    endp = "/pokemon/" + name
    res = await http.get(endp)
    
    if res.status_code == 404:
        return {'details':'Unknown Pokemon'}

    backgroundtask.add_task(RedisClient.set_cache_key, f"cache:pokemon:{name}", res.json())
    print(f"Caching pokemon {name} data", flush=True)
    return res.json()
    
@router.get('/')
async def search_many_pokemon(limit: int = 20, offset: int = 0, http: httpx.AsyncClient = Depends(HTTPXClient.get_http_client)):
    endp = f"/pokemon?limit={limit}&offset={offset}"
    res = await http.get(endp)

    if res.status_code == 404:
        return {'details': 'Unknown endpoint'}

    else:
        return res.json()
    
@router.get('/type/{type}')
async def get_type(type: str, http: httpx.AsyncClient = Depends(HTTPXClient.get_http_client)):
    endp = f"/type/{type}"
    res = await http.get(endp)

    if res.status_code == 404:
        return {'details': 'Unknown endpoint'}

    else:
        return res.json()
    

    