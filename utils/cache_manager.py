from typing import Any, Dict, Optional
from datetime import datetime, timedelta
import yaml
import os
import logging
from functools import wraps
import json
import hashlib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CacheManager:
    def __init__(self):
        self.config = self._load_config()
        self.cache: Dict[str, Dict] = {}
        
    def _load_config(self) -> dict:
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config.yaml')
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def _get_cache_key(self, func_name: str, args: tuple, kwargs: dict) -> str:
        """Generate a unique cache key based on function name and arguments"""
        # Convert args and kwargs to a string representation
        args_str = json.dumps(args, sort_keys=True)
        kwargs_str = json.dumps(kwargs, sort_keys=True)
        
        # Create a unique key using MD5 hash
        key_string = f"{func_name}:{args_str}:{kwargs_str}"
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if it exists and is not expired"""
        if key in self.cache:
            cache_entry = self.cache[key]
            if datetime.now() < cache_entry['expiry']:
                return cache_entry['value']
            else:
                del self.cache[key]
        return None
    
    def set(self, key: str, value: Any, expiry_seconds: int) -> None:
        """Set value in cache with expiration time"""
        self.cache[key] = {
            'value': value,
            'expiry': datetime.now() + timedelta(seconds=expiry_seconds)
        }
    
    def clear(self, pattern: Optional[str] = None) -> None:
        """Clear cache entries matching pattern or all if pattern is None"""
        if pattern is None:
            self.cache.clear()
        else:
            keys_to_delete = [k for k in self.cache.keys() if pattern in k]
            for key in keys_to_delete:
                del self.cache[key]

# Global cache manager instance
cache_manager = CacheManager()

def cached(expiry_seconds: Optional[int] = None):
    """Decorator for caching function results"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get cache duration from config or use provided value
            cache_duration = expiry_seconds or cache_manager.config['cache'].get(
                func.__name__,
                cache_manager.config['cache'].get('default', 300)  # 5 minutes default
            )
            
            # Generate cache key
            cache_key = cache_manager._get_cache_key(func.__name__, args, kwargs)
            
            # Try to get from cache
            cached_value = cache_manager.get(cache_key)
            if cached_value is not None:
                logger.debug(f"Cache hit for {func.__name__}")
                return cached_value
            
            # If not in cache, execute function and cache result
            result = func(*args, **kwargs)
            cache_manager.set(cache_key, result, cache_duration)
            logger.debug(f"Cache miss for {func.__name__}, cached new result")
            
            return result
        return wrapper
    return decorator

def streamlit_cache(ttl_seconds: Optional[int] = None):
    """Decorator specifically for Streamlit functions using st.cache_data"""
    def decorator(func):
        import streamlit as st
        
        # Get cache duration from config or use provided value
        cache_duration = ttl_seconds or cache_manager.config['cache'].get(
            func.__name__,
            cache_manager.config['cache'].get('default', 300)  # 5 minutes default
        )
        
        @st.cache_data(ttl=timedelta(seconds=cache_duration))
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator

def clear_cache(pattern: Optional[str] = None) -> None:
    """Clear cache entries matching pattern or all if pattern is None"""
    cache_manager.clear(pattern)
    
    # Also clear Streamlit cache if running in Streamlit
    try:
        import streamlit as st
        st.cache_data.clear()
    except:
        pass