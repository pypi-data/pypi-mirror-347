from functools import wraps

def cache(func):
    """Decorator to cache method results in a class."""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        cache = getattr(self, '_method_cache', {})
        key = str((func.__name__, args, frozenset(kwargs.items())))
        if key not in cache:
            cache[key] = func(self, *args, **kwargs)
            setattr(self, '_method_cache', cache)
        return cache[key]
    return wrapper