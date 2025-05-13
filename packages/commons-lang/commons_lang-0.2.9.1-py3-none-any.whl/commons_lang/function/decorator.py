import time as t
from typing import Callable
from functools import wraps
from loguru import logger


def elapsed(func) -> Callable:
    def decorator(*args, **kwargs):
        start_time = t.time()
        result = func(*args, **kwargs)
        end_time = t.time()
        logger.debug(f"{func.__name__} elapsed time: {end_time - start_time:.4f} s")
        return result

    return decorator


def deprecated(reason: str) -> Callable:
    def decorator(func) -> Callable:
        original_func = func.__func__ if isinstance(func, staticmethod) or isinstance(func, classmethod) else func

        @wraps(original_func)
        def decorated_function(*args, **kwargs):
            logger.warning(
                f"Call to deprecated function {original_func.__name__}. {reason}",
                category=DeprecationWarning,
                stacklevel=2
            )
            return original_func(*args, **kwargs)

        if isinstance(func, staticmethod):
            return staticmethod(decorated_function)
        elif isinstance(func, classmethod):
            return classmethod(decorated_function)
        else:
            return decorated_function

    return decorator
