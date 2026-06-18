import redis.asyncio as redis

from app.core import ENV

import os 

from dotenv import load_dotenv

load_dotenv()


if ENV == "docker":
    REDIS_HOST = "redis"

else:
    raise ValueError(f"Unknown ENV: {ENV}")


redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=os.getenv("REDIS_PORT") or 6379,
    db=os.getenv("REDIS_DB") or 0,
    decode_responses=True
)