from typing import Any

import pytest

from seminar06.tasks.task02_last_call_cache.last_call_cache import LastCallCache


def test_construction_does_not_call_function() -> None:
    calls: list[int] = []

    def func(value: int) -> int:
        calls.append(value)
        return value * 2

    cached: Any = LastCallCache(func)
    assert calls == []
    assert cached(3) == cached(3) == 6
    assert calls == [3]


def test_only_the_last_call_is_cached() -> None:
    calls: list[int] = []

    def func(value: int) -> int:
        calls.append(value)
        return value * 2

    cached: Any = LastCallCache(func)
    assert [cached(5), cached(5), cached(7), cached(5)] == [10, 10, 14, 10]
    assert calls == [5, 7, 5]


@pytest.mark.parametrize("result", [None, 0, False, "", []])
def test_falsey_results_are_cached(result: Any) -> None:
    calls: list[int] = []

    def func(value: int) -> Any:
        calls.append(value)
        return result

    cached: Any = LastCallCache(func)
    assert cached(0) is result
    assert cached(0) is result
    assert calls == [0]
    assert cached(-1) is result
    assert calls == [0, -1]


def test_hit_returns_the_same_result_object() -> None:
    def func(value: int) -> list[int]:
        return [value]

    cached: Any = LastCallCache(func)
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

    left: Any = LastCallCache(func)
    right: Any = LastCallCache(func)
    left_result = left(2)
    right_result = right(2)
    assert left_result is not right_result
    assert left(2) is left_result
    assert right(2) is right_result
    assert calls == [2, 2]


def test_equal_but_distinct_arguments_hit_cache() -> None:
    calls: list[int] = []

    def func(value: int) -> object:
        calls.append(value)
        return object()

    first, second = int("1000"), int("1000")
    assert first == second and first is not second
    cached: Any = LastCallCache(func)
    result = cached(first)
    assert cached(second) is result
    assert calls == [1000]
