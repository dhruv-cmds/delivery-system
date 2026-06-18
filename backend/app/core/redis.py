import redis.asyncio as redis

from app.core import ENV


if ENV == "docker":
    REDIS_HOST = "redis"

else:
    raise ValueError(f"Unknown ENV: {ENV}")


redis_client = redis.Redis(
    host=REDIS_HOST,
    port=6379,
    db=0,
    decode_responses=True
)