from collections.abc import Callable
from typing import Any


def make_dispatcher(
    commands: dict[str, Callable[..., Any]],
) -> Callable[..., Any]:
    """Создать функцию dispatch(name, /, *args, **kwargs) со своей таблицей команд."""
    raise NotImplementedError("Implement me")
