from collections.abc import Callable
from typing import Any


def rank_items(
    items: list[Any],
    /,
    *,
    score: Callable[[Any], int],
    accept: Callable[[Any], bool] | None = None,
    reverse: bool = True,
) -> list[Any]:
    """Отобрать элементы и упорядочить их по результату score."""
    raise NotImplementedError("Implement me")
