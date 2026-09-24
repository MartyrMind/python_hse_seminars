from collections.abc import Callable
from typing import Any


class TaskQueue:
    def __init__(self) -> None:
        raise NotImplementedError("Implement me")

    def submit(self, func: Callable[..., Any], /, *args: Any, **kwargs: Any) -> None:
        """Сохранить вызов, не выполняя его."""
        raise NotImplementedError("Implement me")

    def run_all(self) -> list[Any]:
        """Выполнить вызовы, находившиеся в очереди на момент старта."""
        raise NotImplementedError("Implement me")
