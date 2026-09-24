from typing import Any

import pytest

from seminar06.tasks.task02_last_call_cache.last_call_cache import LastCallCache


def test_construction_does_not_call_function() -> None:
    calls: list[int] = []

    def func(value: int) -> int:
        calls.append(value)
        return value * 2

    cached = LastCallCache(func)
    assert calls == []
    assert cached(3) == 6
    assert cached(3) == 6
    assert calls == [3]


def test_only_the_last_call_is_cached() -> None:
    calls: list[int] = []

    def func(value: int) -> int:
        calls.append(value)
        return value * 2

    cached = LastCallCache(func)
    assert [cached(5), cached(5), cached(7), cached(5)] == [10, 10, 14, 10]
    assert calls == [5, 7, 5]


def test_positional_and_keyword_arguments_are_forwarded() -> None:
    calls: list[tuple[tuple[int, ...], str, int]] = []

    def func(*values: int, label: str, scale: int = 1) -> str:
        calls.append((values, label, scale))
        return f"{label}:{sum(values) * scale}"

    cached = LastCallCache(func)
    assert cached(2, 3, label="sum", scale=4) == "sum:20"
    assert cached(2, 3, scale=4, label="sum") == "sum:20"
    assert calls == [((2, 3), "sum", 4)]
    assert cached(2, 3, label="sum", scale=5) == "sum:25"
    assert len(calls) == 2


def test_different_call_forms_are_not_normalized() -> None:
    calls: list[int] = []

    def func(x: int = 5) -> int:
        calls.append(x)
        return x

    cached = LastCallCache(func)
    assert cached(5) == cached(x=5) == cached() == 5
    assert calls == [5, 5, 5]
    assert cached() == 5
    assert calls == [5, 5, 5]


@pytest.mark.parametrize("result", [None, 0, False, "", []])
def test_falsey_results_are_cached_even_for_no_arguments(result: Any) -> None:
    calls: list[str] = []

    def func() -> Any:
        calls.append("called")
        return result

    cached = LastCallCache(func)
    assert cached() is result
    assert cached() is result
    assert calls == ["called"]


def test_hit_returns_the_same_result_object() -> None:
    def func(value: int) -> list[int]:
        return [value]

    cached = LastCallCache(func)
    first = cached(1)
    first.append(99)
    assert cached(1) is first
    assert cached(1) == [1, 99]
    assert cached(2) == [2]


def test_instances_do_not_share_a_cache() -> None:
    calls: list[int] = []

    def func(value: int) -> list[int]:
        calls.append(value)
        return [value]

    left = LastCallCache(func)
    right = LastCallCache(func)
    left_result = left(2)
    right_result = right(2)
    assert left_result is not right_result
    assert left(2) is left_result
    assert right(2) is right_result
    assert calls == [2, 2]


def test_keyword_named_self_is_forwarded() -> None:
    def func(**options: str) -> str:
        return options["self"]

    cached = LastCallCache(func)
    assert cached(self="value") == "value"
    assert cached(self="value") == "value"


@pytest.mark.parametrize("named", [False, True], ids=["positional", "keyword"])
def test_equal_but_distinct_argument_values_hit_cache(named: bool) -> None:
    calls: list[float] = []

    def func(value: float) -> object:
        calls.append(value)
        return object()

    first, second = float("1.5"), float("1.5")
    assert first == second
    assert first is not second
    cached = LastCallCache(func)
    if named:
        result = cached(value=first)
        repeated = cached(value=second)
    else:
        result = cached(first)
        repeated = cached(second)
    assert repeated is result
    assert calls == [1.5]
