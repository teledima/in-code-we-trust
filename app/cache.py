import functools
import pickle
from collections.abc import Callable
from time import time


class Cache:
    def __init__(self):
        self.cache = {}

    def add(self, key, value, ttl):
        self.cache[key] = pickle.dumps((int(time() + ttl), value))

    def get(self, key):
        if key not in self.cache:
            return None

        expires, value = pickle.loads(self.cache[key])

        if expires < int(time()):
            return None

        return value

    def cached(self, ttl: int, key_factory: Callable):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                key = func.__name__ + key_factory(*args, **kwargs)
                cached = self.get(key)
                if cached is None:
                    self.add(key, func(*args, **kwargs), ttl)
                    return self.get(key)
                return cached
            return wrapper
        return decorator


cache = Cache()
