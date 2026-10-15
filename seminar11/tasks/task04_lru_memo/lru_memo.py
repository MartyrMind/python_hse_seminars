from collections.abc import Callable
from typing import Protocol


class Cached[**P, R](Protocol):
    hits: int
    misses: int
    cache_size: Callable[[], int]
    cache_clear: Callable[[], None]

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R: ...


class LRUMemo:
    def __init__(self, capacity: int) -> None:
        raise NotImplementedError("Implement me")

    def __call__[**P, R](self, func: Callable[P, R]) -> Cached[P, R]:
        raise NotImplementedError("Implement me")
