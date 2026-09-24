from collections.abc import Callable
from typing import Any

Command = Callable[..., Any] | str


def make_dispatcher(
    commands: dict[str, Command],
) -> Callable[..., Any]:
    """Создать диспетчер функций и псевдонимов команд."""
    raise NotImplementedError("Implement me")
