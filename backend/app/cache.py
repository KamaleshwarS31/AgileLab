import redis
import json
from typing import Optional, Any
from app.config import settings

# Create Redis client
redis_client = redis.from_url(
    settings.redis_url,
    decode_responses=True,
    socket_connect_timeout=5,
    socket_timeout=5
)


class Cache:
    """Redis cache manager"""
    
    @staticmethod
    def get(key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            value = redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            print(f"Cache get error: {e}")
            return None
    
    @staticmethod
    def set(key: str, value: Any, expiration: int = None) -> bool:
        """Set value in cache with optional expiration"""
        try:
            expiration = expiration or settings.cache_expiration
            redis_client.setex(
                key,
                expiration,
                json.dumps(value)
            )
            return True
        except Exception as e:
            print(f"Cache set error: {e}")
            return False
    
    @staticmethod
    def delete(key: str) -> bool:
        """Delete key from cache"""
        try:
            redis_client.delete(key)
            return True
        except Exception as e:
            print(f"Cache delete error: {e}")
            return False
    
    @staticmethod
    def clear_pattern(pattern: str) -> int:
        """Clear all keys matching pattern"""
        try:
            keys = redis_client.keys(pattern)
            if keys:
                return redis_client.delete(*keys)
            return 0
        except Exception as e:
            print(f"Cache clear error: {e}")
            return 0


cache = Cache()
