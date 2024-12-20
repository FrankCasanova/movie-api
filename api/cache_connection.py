# conection to redis
from redis.asyncio import Redis


async def get_redis():
    redis = Redis(host="redis", port=6379, db=0)
    return redis
