from collections.abc import Callable
from inspect import unwrap
from typing import Any

import pytest

from seminar11.tasks.task01_trimmed.trimmed import trimmed

pytestmark = pytest.mark.timeout(5)


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("  привет \n", "привет"),
        ("\t\u2003текст\u00a0", "текст"),
        (" a  b\nc ", "a  b\nc"),
        ("", ""),
        (" \n\t", ""),
        ("готово", "готово"),
    ],
)
def test_only_outer_whitespace_is_removed(text: str, expected: str) -> None:
    @trimmed
    def read() -> str:
        return text

    assert read() == expected


def test_arguments_pass_through_and_function_runs_once_per_call() -> None:
    calls: list[tuple[str, str]] = []

    @trimmed
    def greet(name: str, /, *, punctuation: str = "!") -> str:
        calls.append((name, punctuation))
        return f"  Привет, {name}{punctuation} \n"

    assert calls == []
    assert greet("Аня", punctuation="?") == "Привет, Аня?"
    assert greet("Боря") == "Привет, Боря!"
    assert calls == [("Аня", "?"), ("Боря", "!")]


def test_metadata_and_original_function_are_preserved() -> None:
    def title() -> str:
        """Название отчёта."""
        return "  Отчёт  "

    wrapped = trimmed(title)
    assert wrapped.__name__ == "title"
    assert wrapped.__doc__ == "Название отчёта."
    assert unwrap(wrapped) is title
    assert title() == "  Отчёт  "
    assert wrapped() == "Отчёт"


def test_original_exception_is_not_replaced() -> None:
    error = RuntimeError("источник недоступен")
    calls = 0

    @trimmed
    def read() -> str:
        nonlocal calls
        calls += 1
        raise error

    with pytest.raises(RuntimeError) as caught:
        read()
    assert caught.value is error
    assert calls == 1


@pytest.mark.parametrize("layers", [1, 2])
def test_wraps_preserves_full_metadata_at_each_layer(
    layers: int, assert_metadata: Callable[[Any, Any], None]
) -> None:
    def title[T](value: T, /, *, suffix: str = "!") -> str:
        """Название отчёта."""
        return f"  {value}{suffix}  "

    title.__dict__["audit_tag"] = object()
    wrapped = title
    for _ in range(layers):
        original = wrapped
        wrapped = trimmed(original)
        assert_metadata(wrapped, original)

    assert wrapped("Отчёт", suffix="?") == "Отчёт?"
