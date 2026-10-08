from collections.abc import Iterable, Iterator
from typing import NamedTuple


class Tagged[T](NamedTuple):
    number: int
    label: str
    value: T


def tag_stream[T](
    batches: Iterable[Iterable[T]], labels: tuple[str, ...], limit: int, start: int = 1
) -> Iterator[Tagged[T]]:
    raise NotImplementedError("Implement me")
