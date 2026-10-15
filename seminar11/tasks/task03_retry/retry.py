from collections.abc import Callable
from typing import Protocol


class RetryDecorator(Protocol):
    def __call__[**P, R](self, func: Callable[P, R], /) -> Callable[P, R]: ...


def retry(attempts: int, errors: tuple[type[Exception], ...]) -> RetryDecorator:
    raise NotImplementedError("Implement me")
