# 🐍 PokeCache API — FastAPI + Redis + HTTPX

A high-performance **FastAPI** service that caches responses from the [PokéAPI](https://pokeapi.co/) using **Redis** to drastically improve response times and reduce redundant network requests.

Built with the purpose of learning Redis and Docker implementation.

---

## 🚀 Features

- **FastAPI** backend with async I/O  
- **HTTPX** client for efficient async requests  
- **Redis caching** layer with TTL control  
- **Background caching** (non-blocking response writes)  
- **Connection pooling** for both Redis and HTTP clients  
- **Docker-ready** architecture  
- Clean, reusable **singleton client pattern** for shared connections  

---

## 🧠 How It Works

1. When a request comes in (e.g. `/pokemon?name=pikachu`):
   - The app first checks Redis for a cached copy.
   - If found → returns instantly with header `X-CACHE: HIT`.
   - If not → fetches from PokéAPI → returns data → stores it in Redis in the background with `X-CACHE: MISS`.

2. The next time the same Pokémon is requested, it will load **directly from cache**, skipping PokéAPI entirely.

This ensures **faster responses** and **lower API latency**.

---

## 🧩 Project Structure

app/
├── cache.py # Redis client (singleton pattern)
├── endpoints.py # API route handlers
├── httpxclient.py # Shared async HTTPX client (also singleton pattern)
└── main.py # FastAPI app entry point with lifespan context

## 📦 API Endpoints

| Endpoint | Method | Description |
|-----------|---------|-------------|
| `/pokemon?name=<name>` | `GET` | Fetch Pokémon by name. Uses Redis cache. |
| `/type/{type}` | `GET` | Fetch Pokémon type details. Cached as well. |
| `/` | `GET` | Paginated list of Pokémon (limit & offset). |

## 💡 Future Improvements

- Add TTL configuration for selective caching
- Integrate compression for large payloads (Zstandard)

## Setup
`
docker compose up --build
`

App will be available at: 👉 http://localhost:8000