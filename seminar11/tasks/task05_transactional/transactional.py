from collections.abc import Callable
from contextlib import AbstractContextManager


class Transactions[K, V]:
    def __init__(self, state: dict[K, V]) -> None:
        raise NotImplementedError("Implement me")

    def atomic(self) -> AbstractContextManager[dict[K, V]]:
        raise NotImplementedError("Implement me")

    def transactional[**P, R](self, func: Callable[P, R]) -> Callable[P, R]:
        raise NotImplementedError("Implement me")
