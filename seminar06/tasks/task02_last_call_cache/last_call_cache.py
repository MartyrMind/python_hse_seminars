from collections.abc import Callable
from typing import Any


class LastCallCache:
    def __init__(self, func: Callable[..., Any]) -> None:
        raise NotImplementedError("Implement me")

    def __call__(self, /, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError("Implement me")
