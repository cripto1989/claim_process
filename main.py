from math import ceil
from fastapi_limiter import FastAPILimiter
import redis.asyncio as redis
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request, Response, status
from db import create_all_tables
from src.api.router import v1_router


async def service_name_identifier(request: Request):
    service = request.headers.get("Service-Name")
    return service


async def custom_callback(request: Request, response: Response, pexpire: int):
    expire = ceil(pexpire / 1000)

    raise HTTPException(
        status.HTTP_429_TOO_MANY_REQUESTS,
        f"Too Many Requests. Retry after {expire} seconds.",
        headers={"Retry-After": str(expire)},
    )

@asynccontextmanager
async def app_lifespan(app: FastAPI):
    redis_connection = redis.from_url("redis://redis:6379/0", encoding="utf8")
    await FastAPILimiter.init(
        redis=redis_connection,
        identifier=service_name_identifier,
        http_callback=custom_callback,
    )

    print("init lifespan")
    create_all_tables()
    yield
    await FastAPILimiter.close()
    print("clean up lifespan")

app = FastAPI(lifespan=app_lifespan)

app.include_router(v1_router, prefix="/api/v1")
