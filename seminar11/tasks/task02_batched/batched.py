from collections.abc import Callable, Iterable
from typing import Concatenate, Protocol


class BatchDecorator(Protocol):
    def __call__[T, R, **P](
        self, func: Callable[Concatenate[list[T], P], list[R]], /
    ) -> Callable[Concatenate[Iterable[T], P], list[R]]: ...


def batched(size: int) -> BatchDecorator:
    raise NotImplementedError("Implement me")
