import json
import traceback
from functools import wraps
from typing import Callable

from aiocache import Cache
from aiocache.serializers import PickleSerializer
from fastapi import Path

from cores.logger.logging import ApiLogger


def handle_exception(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception:
            ApiLogger.logging_curl(traceback.format_exc())
            return None

    return wrapper


class CacheHandler:
    def __init__(self):
        self.cache = Cache(
            Cache.MEMCACHED,  # type: ignore
            endpoint="memcache",
            port=11211,
            serializer=PickleSerializer(),
        )
        self.cache_key_file = Path("cache_keys.json")
        self.keys = set()

        if not self.cache_key_file.exists():
            self.cache_key_file.write_text(json.dumps([]))

        self._load_keys()

    @handle_exception
    async def get(self, key):
        value = await self.cache.get(key)  # type: ignore
        return value

    @handle_exception
    async def set(self, key, value, ttl=3600):
        await self.cache.set(key, value, ttl=ttl)  # type: ignore
        self._add_key_to_file(key)

    @handle_exception
    async def delete(self, key):
        await self.cache.delete(key)  # type: ignore
        self._remove_key_from_file(key)

    @handle_exception
    async def health_check(self):
        try:
            await self.set("key", "value")
            value = await self.get("key")
            return value == "value"
        except Exception:
            return False

    def _load_keys(self):
        """Tải key từ file JSON vào bộ nhớ."""
        try:
            with open(self.cache_key_file, "r") as f:
                self.keys = set(json.load(f))
        except Exception as e:
            ApiLogger.logging_curl(f"Error loading keys from file: {e}")

    def _add_key_to_file(self, key):
        if key not in self.keys:
            self.keys.add(key)
            self._write_keys()

    def _remove_key_from_file(self, key):
        if key in self.keys:
            self.keys.remove(key)
            self._write_keys()

    def _write_keys(self):
        """Ghi danh sách key vào file JSON."""
        try:
            with open(self.cache_key_file, "w") as f:
                json.dump(list(self.keys), f, indent=4)
        except Exception as e:
            ApiLogger.logging_curl(f"Error writing keys to file: {e}")

    async def close(self):
        """Đóng kết nối khi ứng dụng kết thúc."""
        await self.cache.close()  # type: ignore


cache_handler = CacheHandler()


def list_cacheable(cache_key_prefix: str, key_to_cache: str = "id", ttl=3600):
    """
    Decorator kiểm tra cache trước khi gọi hàm gốc.
    Nếu cache có, trả về giá trị từ cache.
    Nếu không, gọi hàm gốc và lưu kết quả vào cache.
    """

    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Nếu key ko phải là dạng list[int] thì return []
            if len(args) < 1 or not isinstance(args[1], list):
                return []

            # args[1] là ids
            results = []  # Danh sách chứa cache value

            # Tạo một danh sách tạm để lưu lại các id chưa có trong cache
            remaining_ids = []

            for item_id in args[1]:
                cache_key = f"{cache_key_prefix}:{item_id}"
                # Kiểm tra cache
                cached_value = await cache_handler.get(cache_key)

                if cached_value is not None:
                    results.append(cached_value)  # Lưu giá trị đã cache
                else:
                    remaining_ids.append(item_id)  # Lưu lại ID chưa cache

            # Gọi hàm gốc để lấy data nếu chưa có cache.
            if remaining_ids:
                origin_results = await func(args[0], remaining_ids)
                if origin_results is not None:
                    mapping = {}
                    for item in origin_results:
                        mapping[getattr(item, key_to_cache)] = item
                        cache_key = (
                            f"{cache_key_prefix}:{getattr(item, key_to_cache)}"
                        )
                        await cache_handler.set(cache_key, item, ttl)
                        results.append(item)
            await cache_handler.close()
            return results

        return wrapper

    return decorator


def cacheable(cache_key_prefix):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = (
                f"{cache_key_prefix}_{args[0]}" if args else cache_key_prefix
            )
            data = await cache_handler.get(cache_key)
            if data is not None:
                return data

            data = await func(*args, **kwargs)
            await cache_handler.set(cache_key, data)
            await cache_handler.close()
            return data

        return wrapper

    return decorator
