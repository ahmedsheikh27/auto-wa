import redis
from app.core.config import Settings
REDIS_URL = Settings.REDIS_URL

redis_client = redis.Redis.from_url(
    REDIS_URL,
    decode_responses=True
)