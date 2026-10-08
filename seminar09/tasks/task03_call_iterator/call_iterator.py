from collections.abc import Callable
from typing import Self


class CallIterator[T]:
    def __init__(self, source: Callable[[], T], sentinel: object) -> None:
        raise NotImplementedError("Implement me")

    def __iter__(self) -> Self:
        raise NotImplementedError("Implement me")

    def __next__(self) -> T:
        raise NotImplementedError("Implement me")
