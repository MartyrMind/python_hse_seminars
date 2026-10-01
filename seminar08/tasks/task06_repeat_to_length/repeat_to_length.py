from collections.abc import Iterable
from typing import Any, Protocol


class RepeatableSized(Protocol):
    """Протокол фрагмента, который можно повторять до нужной длины."""


class RepeatLengthError(ValueError):
    """Длина результата нарушила договор о повторении."""


def repeat_to_length(value: Any, minimum: int) -> Any:
    raise NotImplementedError("Implement me")


def repeat_all(values: Iterable[Any], minimum: int) -> list[Any]:
    raise NotImplementedError("Implement me")
