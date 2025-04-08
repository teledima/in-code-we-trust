import functools
import pickle
from collections.abc import Callable
from time import time


class Cache:
    """Класс для кэширования данных в памяти с поддержкой TTL (время жизни)."""

    def __init__(self):
        # Инициализация хранилища кэша (словарь)
        self.cache = {}

    def add(self, key, value, ttl):
        """
        Добавляет значение в кэш с указанным временем жизни (TTL).

        Args:
            key: Ключ для сохранения значения
            value: Данные для кэширования
            ttl: Time-To-Live (в секундах), сколько данные должны храниться в кэше
        """
        # Сериализуем кортеж (время истечения, значение) и сохраняем в кэш
        self.cache[key] = pickle.dumps((int(time() + ttl), value))

    def get(self, key):
        """
        Получает значение из кэша по ключу.

        Args:
            key: Ключ для поиска в кэше

        Returns:
            Значение, если оно есть в кэше и не истекло, иначе None
        """
        # Если ключа нет в кэше, возвращаем None
        if key not in self.cache:
            return None

        expires, value = pickle.loads(self.cache[key])

        # Проверяем, не истекло ли время жизни данных
        if expires < int(time()):
            return None

        return value

    def cached(self, ttl: int, key_factory: Callable):
        """
        Декоратор для кэширования результатов функции.

        Args:
            ttl: Время жизни кэша в секундах
            key_factory: Функция для генерации ключа кэша
        """
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # Генерируем ключ кэша: имя функции + результат key_factory
                key = func.__name__ + key_factory(*args, **kwargs)

                # Получаем значение из кэша
                cached = self.get(key)

                # Если значение есть в кэше, возвращаем его, иначе вызываем функцию и сохраняем результат в кэш
                if cached is None:
                    self.add(key, func(*args, **kwargs), ttl)
                    return self.get(key)
                return cached
            return wrapper
        return decorator


cache = Cache()
