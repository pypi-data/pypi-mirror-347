import random
import time
from functools import wraps
from typing import Type, Callable, TypeVar, ParamSpec
from .exceptions import RagtasticError, RateLimitError

P = ParamSpec("P")
T = TypeVar("T")


def retry_with_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    jitter: bool = True,
    retryable_exceptions: tuple[Type[Exception], ...] = (RateLimitError,),
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """
    Decorator that implements exponential backoff with optional jitter

    Args:
        max_retries: Maximum number of retries
        base_delay: Initial delay between retries in seconds
        max_delay: Maximum delay between retries in seconds
        jitter: Whether to add random jitter to delay
        retryable_exceptions: Tuple of exceptions that should trigger a retry
    """

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            retries = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except retryable_exceptions as e:
                    retries += 1
                    if retries > max_retries:
                        raise RagtasticError(
                            f"Max retries ({max_retries}) exceeded"
                        ) from e

                    delay = min(base_delay * (2 ** (retries - 1)), max_delay)

                    if jitter:
                        delay = delay * (0.5 + random.random())

                    time.sleep(delay)
                except Exception as e:
                    raise RagtasticError(f"Unhandled error: {str(e)}") from e

        return wrapper

    return decorator
