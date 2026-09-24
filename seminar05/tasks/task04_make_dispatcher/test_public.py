from collections.abc import Callable
from typing import Any

from seminar05.tasks.task04_make_dispatcher.make_dispatcher import make_dispatcher


def test_creation_does_not_call_handlers_and_dispatch_calls_only_selected() -> None:
    calls: list[str] = []

    def first() -> str:
        calls.append("first")
        return "one"

    def second() -> str:
        calls.append("second")
        return "two"

    dispatch = make_dispatcher({"first": first, "second": second})
    assert calls == []
    assert dispatch("second") == "two"
    assert calls == ["second"]


def test_dispatch_forwards_arguments_and_returns_original_result() -> None:
    result: list[int] = []

    def handler(x: int, /, *, name: str, commands: str) -> list[int]:
        assert (x, name, commands) == (3, "payload", "also payload")
        return result

    dispatch = make_dispatcher({"run": handler})
    assert dispatch("run", 3, name="payload", commands="also payload") is result


def test_unknown_name_returns_none_without_calling_anything() -> None:
    def unexpected() -> None:
        raise AssertionError("Неизвестная команда не должна вызывать обработчик")

    dispatch = make_dispatcher({"known": unexpected})
    assert dispatch("absent", 1, name=2) is None
    assert make_dispatcher({})("anything") is None


def test_each_dispatcher_keeps_its_own_snapshot_of_command_mapping() -> None:
    def old() -> str:
        return "old"

    def new() -> str:
        return "new"

    commands: dict[str, Callable[..., Any]] = {"run": old}
    first = make_dispatcher(commands)
    commands["run"] = new
    commands["extra"] = new
    second = make_dispatcher(commands)
    commands.clear()
    assert first("run") == "old"
    assert first("extra") is None
    assert second("run") == "new"
    assert second("extra") == "new"
    assert first("run") == "old"


def test_bound_handler_keeps_reference_to_live_instance() -> None:
    class Counter:
        def __init__(self) -> None:
            self.value = 0

        def add(self, amount: int) -> int:
            self.value += amount
            return self.value

    counter = Counter()
    dispatch = make_dispatcher({"add": counter.add})
    counter.value = 10
    assert dispatch("add", 2) == 12
    assert dispatch("add", 3) == 15
    assert counter.value == 15
