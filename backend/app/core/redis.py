import redis
from .config import settings

redis_client = redis.Redis.from_url(settings.REDIS_URL)