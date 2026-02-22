from redis import Redis
from app.common.config.settings import settings

redis_client = Redis.from_url(settings.redis_dsn, decode_responses=True)