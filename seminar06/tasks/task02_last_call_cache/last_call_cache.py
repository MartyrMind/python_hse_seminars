from collections.abc import Callable
from typing import Any


class LastCallCache:
    def __init__(self, func: Callable[[int], Any]) -> None:
        raise NotImplementedError("Implement me")
