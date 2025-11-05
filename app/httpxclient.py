import httpx

class HTTPXClient:
    
    _instance: httpx.AsyncClient | None = None

    @classmethod
    async def init(cls, url):
        cls._instance = httpx.AsyncClient(base_url=url)

    @classmethod
    async def get_http_client(cls) -> httpx.AsyncClient:
        return cls._instance
    
    @classmethod
    async def close_conn(cls):
        await cls._instance.aclose()