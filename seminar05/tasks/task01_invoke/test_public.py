from typing import Any

from seminar05.tasks.task01_invoke.invoke import invoke


def test_forwards_positional_and_keyword_only_arguments() -> None:
    def calculate(x: int, /, y: int = 2, *, scale: int = 1) -> int:
        return (x + y) * scale

    assert invoke(calculate, 3, y=4, scale=2) == 14
    assert invoke(calculate, 3) == 5


def test_parameter_name_does_not_steal_payload_keywords() -> None:
    def payload(**values: Any) -> dict[str, Any]:
        return values

    assert invoke(payload, func="report", args=1, kwargs=2) == {
        "func": "report",
        "args": 1,
        "kwargs": 2,
    }


def test_no_arguments_calls_exactly_once_and_preserves_result_identity() -> None:
    calls: list[str] = []
    result: list[int] = []

    def produce() -> list[int]:
        calls.append("called")
        return result

    assert invoke(produce) is result
    assert calls == ["called"]


def test_argument_objects_are_not_copied() -> None:
    target: list[int] = []

    def add(values: list[int], *, extra: list[int]) -> list[int]:
        assert values is target
        assert extra is target
        values.append(7)
        return values

    assert invoke(add, target, extra=target) is target
    assert target == [7]


def test_bound_method_already_remembers_its_instance() -> None:
    values: list[int] = []
    assert invoke(values.append, 5) is None
    assert values == [5]
