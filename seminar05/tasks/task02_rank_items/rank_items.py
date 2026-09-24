from collections.abc import Callable
from typing import Any


def rank_items(
    items: list[Any],
    /,
    *,
    criteria: list[tuple[Callable[[Any], int], bool]],
    accept: Callable[[Any], bool] | None = None,
) -> list[Any]:
    """Отобрать элементы и упорядочить по нескольким критериям."""
    raise NotImplementedError("Implement me")
