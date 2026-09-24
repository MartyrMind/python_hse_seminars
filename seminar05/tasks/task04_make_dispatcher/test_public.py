from collections.abc import Callable
from typing import Any

import pytest

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

    commands: dict[str, Callable[..., Any] | str] = {"run": old}
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


def test_alias_chain_forwards_arguments_once_to_final_handler() -> None:
    calls: list[int] = []
    result: list[int] = []

    def handler(x: int, *, name: str) -> list[int]:
        assert name == "payload"
        calls.append(x)
        return result

    dispatch = make_dispatcher({"short": "alias", "alias": "run", "run": handler})
    assert calls == []
    assert dispatch("short", 7, name="payload") is result
    assert calls == [7]
    assert dispatch("alias", 8, name="payload") is result
    assert calls == [7, 8]


def test_alias_to_missing_command_returns_none() -> None:
    dispatch = make_dispatcher({"short": "missing"})
    assert dispatch("short", 1, name="anything") is None


@pytest.mark.timeout(1)
def test_cycles_return_none_and_do_not_break_other_commands() -> None:
    dispatch = make_dispatcher({"a": "b", "b": "a", "self": "self", "entry": "a", "number": int})
    assert dispatch("a") is None
    assert dispatch("self") is None
    assert dispatch("entry") is None
    assert dispatch("number", "7") == 7
    assert dispatch("a") is None


def test_alias_targets_are_fixed_with_the_rest_of_the_table() -> None:
    commands: dict[str, Callable[..., Any] | str] = {"short": "text", "text": str}
    first = make_dispatcher(commands)
    commands["text"] = int
    second = make_dispatcher(commands)
    commands.clear()
    assert first("short", 7) == "7"
    assert second("short", "7") == 7


def test_empty_string_can_be_an_alias_target() -> None:
    dispatch = make_dispatcher({"short": "", "": len})
    assert dispatch("short", [1, 2]) == 2
