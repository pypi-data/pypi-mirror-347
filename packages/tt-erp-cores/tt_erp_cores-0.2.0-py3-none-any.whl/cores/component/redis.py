from typing import Any, Optional

import aioredis

from cores.configs.api_configs import Config


class RedisHandler:
    def __init__(
        self,
        host: str = Config.REDIS_HOST,
        port: int = Config.REDIS_PORT,
        password: str = Config.REDIS_PASSWORD,
        db: int = Config.REDIS_DB,
    ):
        self._address = f"redis://{host}:{port}/{db}"
        self._password = password
        self.client = None

    async def initialize(self):
        """Khởi tạo kết nối Redis khi cần."""
        if self.client is None or self.client.closed:
            self.client = await aioredis.create_redis_pool(
                self._address,
                password=self._password,
                encoding="utf-8",  # Decode responses thành string
            )

    async def set(
        self, key: str, value: Any, ex: Optional[int] = None
    ) -> bool:
        """SET key value"""
        await self.initialize()
        return await self.client.set(key, value, expire=ex)

    async def get(self, key: str) -> Optional[str]:
        """GET key"""
        await self.initialize()
        return await self.client.get(key)

    async def delete(self, key: str) -> int:
        """DELETE key"""
        await self.initialize()
        return await self.client.delete(key)

    async def exists(self, key: str) -> bool:
        """EXISTS key"""
        await self.initialize()
        return await self.client.exists(key)

    async def ttl(self, key: str) -> int:
        """TTL key"""
        await self.initialize()
        return await self.client.ttl(key)

    async def incr(self, key: str) -> int:
        """INCR key"""
        await self.initialize()
        return await self.client.incr(key)

    async def hset(self, key: str, field: str, value: Any) -> int:
        """HSET key field value"""
        await self.initialize()
        return await self.client.hset(key, field, value)

    async def hget(self, key: str, field: str) -> Optional[str]:
        """HGET key field"""
        await self.initialize()
        return await self.client.hget(key, field)

    async def hgetall(self, key: str) -> dict[str, str]:
        """HGETALL key"""
        await self.initialize()
        return await self.client.hgetall(key)

    async def lpush(self, key: str, *values: Any) -> int:
        """LPUSH key value"""
        await self.initialize()
        return await self.client.lpush(key, *values)

    async def lrange(self, key: str, start: int, stop: int) -> list[str]:
        """LRANGE key start stop"""
        await self.initialize()
        return await self.client.lrange(key, start, stop)

    async def expire(self, key: str, seconds: int) -> bool:
        """EXPIRE key seconds"""
        await self.initialize()
        return await self.client.expire(key, seconds)

    async def flushdb(self) -> bool:
        """FLUSHDB"""
        await self.initialize()
        return await self.client.flushdb()

    async def close(self):
        """Đóng kết nối Redis"""
        if self.client and not self.client.closed:
            self.client.close()
            await self.client.wait_closed()


# Singleton instance
redis_handler = RedisHandler()


# Khởi tạo Redis khi ứng dụng khởi động (dùng trong lifespan nếu cần)
async def get_redis() -> RedisHandler:
    await redis_handler.initialize()
    return redis_handler
