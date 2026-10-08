from collections.abc import Iterator
from typing import Literal

type Mode = Literal["product", "permutations", "combinations", "replacement"]


def candidate_codes(
    alphabet: str, length: int, mode: Mode, forbidden: tuple[str, ...] = (), limit: int = 10
) -> Iterator[str]:
    raise NotImplementedError("Implement me")
