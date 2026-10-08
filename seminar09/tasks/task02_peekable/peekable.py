from collections.abc import Iterable
from typing import Self


class Peekable[T]:
    def __init__(self, source: Iterable[T]) -> None:
        raise NotImplementedError("Implement me")

    def __iter__(self) -> Self:
        raise NotImplementedError("Implement me")

    def __next__(self) -> T:
        raise NotImplementedError("Implement me")

    def peek(self) -> T:
        raise NotImplementedError("Implement me")
