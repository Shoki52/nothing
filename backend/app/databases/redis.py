import redis.asyncio as redis
from app.configs.config import RedisSettings

redisSettings = RedisSettings()
jwt_users = redis.Redis(host=redisSettings.RD_SERVER, port=6379, db=2, password=redisSettings.RD_PASSWORD)
jwt_admins = redis.Redis(host=redisSettings.RD_SERVER, port=6379, db=3, password=redisSettings.RD_PASSWORD)

