from fastapi import APIRouter, Depends
import httpx
from app.dependencies import get_http_client

API_URL = "https://pokeapi.co/api/v2/"

router = APIRouter()

@router.get("/pokemon") # /pokemon?name=Pikachu
async def get_pokemon_by_name(name: str, http: httpx.AsyncClient = Depends(get_http_client)):
    endp = "/pokemon/" + name
    res = await http.get(endp)
    
    if res.status_code == 404:
        return {'details':'Unknown Pokemon'}

    else:
        return res.json()
    
@router.get('/')
async def search_many_pokemon(limit: int = 20, offset: int = 0, http: httpx.AsyncClient = Depends(get_http_client)):
    endp = f"/pokemon?limit={limit}&offset={offset}"
    res = await http.get(endp)

    if res.status_code == 404:
        return {'details': 'Unknown endpoint'}

    else:
        return res.json()
    
@router.get('/type/{type}')
async def get_type(type: str, http: httpx.AsyncClient = Depends(get_http_client)):
    endp = f"/type/{type}"
    res = await http.get(endp)

    if res.status_code == 404:
        return {'details': 'Unknown endpoint'}

    else:
        return res.json()
    

    