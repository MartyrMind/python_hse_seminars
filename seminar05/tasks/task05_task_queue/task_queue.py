from collections.abc import Callable
from typing import Any


class Result:
    def __init__(self) -> None:
        self.ready: bool
        self.value: Any
        raise NotImplementedError("Implement me")


class TaskQueue:
    def __init__(self) -> None:
        raise NotImplementedError("Implement me")

    def submit(self, func: Callable[..., Any], /, *args: Any, **kwargs: Any) -> Result:
        """Сохранить вызов и вернуть объект для его будущего результата."""
        raise NotImplementedError("Implement me")

    def run_all(self) -> list[Any]:
        """Выполнить вызовы, находившиеся в очереди на момент старта."""
        raise NotImplementedError("Implement me")
