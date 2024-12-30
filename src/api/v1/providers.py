import json
import redis
from fastapi import APIRouter, Depends, status
from fastapi_limiter.depends import RateLimiter
from sqlmodel import select
from db import SessionDep
from src.models import ProviderAverage

redis_client = redis.Redis(host='redis', port=6379, db=0)

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK, dependencies=[Depends(RateLimiter(times=10, seconds=60))])
def get_providers(session: SessionDep):
    cached_providers = redis_client.get("providers")

    if cached_providers:
        print(f"Recovering from cache")        
        return json.loads(cached_providers)

    statement = select(ProviderAverage).order_by(ProviderAverage.average).limit(10)
    providers = session.exec(statement).all()

    providers = json.dumps([row.model_dump() for row in providers])
    redis_client.set(f"providers", providers, 300)

    return json.loads(providers)
