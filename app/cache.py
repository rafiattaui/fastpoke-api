from redis import asyncio as aioredis
from redis.exceptions import ConnectionError
import json
from typing import Any, Optional

class RedisClient:
    _instance: Optional[aioredis.Redis] = None

    @classmethod
    async def init(cls, host="redis", port=6379, db=0):
        """Initialize and store a shared Redis instance"""
        cls._instance = aioredis.Redis(host=host, port=port, db=db, decode_responses=True)
        try:
            if await cls._instance.ping():
                print("✅ Connected to Redis server", flush=True)
        except ConnectionError as e:
            print(f"❌ Redis connection failed: {e}", flush=True)
        return cls

    @classmethod
    def get_instance(cls) -> aioredis.Redis:
        if cls._instance is None:
            raise RuntimeError("RedisClient not initialized. Call await RedisClient.init() first.")
        return cls._instance

    @classmethod
    async def set_cache_key(cls, key: str, data: Any, ex: Optional[int] = None):
        try:
            value = json.dumps(data) if isinstance(data, dict) else str(data)
            await cls._instance.set(key, value, ex=ex)
        except Exception as e:
            print(f"Error setting cache for key {key}: {e}", flush=True)

    @classmethod
    async def get_cache_by_key(cls, key: str) -> Optional[dict]:
        try:
            data = await cls._instance.get(key)
            if data:
                try:
                    return json.loads(data)
                except json.JSONDecodeError:
                    return data  # not JSON
            return None
        except Exception as e:
            print(f"Error fetching cache for key {key}: {e}", flush=True)

    @classmethod
    async def close_conn(cls, flush: bool = False):
        if flush:
            await cls._instance.flushall()
        await cls._instance.aclose()

