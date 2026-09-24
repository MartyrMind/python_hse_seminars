from collections.abc import Callable
from typing import Any


def invoke(func: Callable[..., Any], /, *args: Any, **kwargs: Any) -> Any:
    """Вызвать func с переданными аргументами и вернуть её результат."""
    raise NotImplementedError("Implement me")
