from collections.abc import Callable
from typing import Any


def callback(func: Callable[[...], Any]) -> Callable[[...], Any]:
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    wrapper._callback = True
    return wrapper
