import io
from functools import partial
from typing import Any

import pytest

from seminar09.tasks.task03_call_iterator.call_iterator import CallIterator

pytestmark = pytest.mark.timeout(5)


def test_calls_are_lazy_and_stop_before_the_signal() -> None:
    readings = iter([10, None, 20, "STOP", 99])
    calls: list[int] = []

    def read() -> Any:
        calls.append(1)
        return next(readings)

    walk = CallIterator(read, "STOP")
    assert calls == []
    assert iter(walk) is walk
    assert next(walk) == 10
    assert calls == [1]
    assert list(walk) == [None, 20]
    assert len(calls) == 4
    for _ in range(3):
        with pytest.raises(StopIteration):
            next(walk)
    assert len(calls) == 4
    assert next(readings) == 99


@pytest.mark.parametrize("sentinel", [0.0, ["stop"]])
def test_signal_uses_equality_not_identity(sentinel: object) -> None:
    signal: object = 0 if sentinel == 0.0 else ["stop"]
    assert signal is not sentinel
    values = iter([signal, "unread"])
    walk = CallIterator(lambda: next(values), sentinel)
    assert list(walk) == []
    assert next(values) == "unread"


def test_partial_adapts_a_function_with_arguments() -> None:
    text = io.StringIO("abcdefg")
    walk = CallIterator(partial(text.read, 3), "")
    assert list(walk) == ["abc", "def", "g"]


def test_source_stop_iteration_is_final() -> None:
    calls = 0

    def read() -> int:
        nonlocal calls
        calls += 1
        if calls == 1:
            raise StopIteration
        return 99

    walk = CallIterator(read, -1)
    for _ in range(3):
        with pytest.raises(StopIteration):
            next(walk)
    assert calls == 1


def test_source_error_propagates_but_allows_retry() -> None:
    failure = ValueError("временная ошибка")
    calls = 0

    def read() -> int:
        nonlocal calls
        calls += 1
        if calls == 1:
            raise failure
        return 7

    walk = CallIterator(read, 0)
    with pytest.raises(ValueError) as caught:
        next(walk)
    assert caught.value is failure
    assert next(walk) == 7
    assert calls == 2


def test_comparison_error_propagates_without_reusing_the_value() -> None:
    failure = RuntimeError("сравнение сломано")

    class BrokenEquality:
        def __eq__(self, other: object) -> bool:
            raise failure

    readings = iter([BrokenEquality(), 7, 0])
    walk = CallIterator(lambda: next(readings), 0)
    with pytest.raises(RuntimeError) as caught:
        next(walk)
    assert caught.value is failure
    assert next(walk) == 7
    assert list(walk) == []


def test_zero_and_none_are_data_when_the_signal_is_different() -> None:
    readings = iter([0, None, False, "", "STOP"])
    assert list(CallIterator(lambda: next(readings), "STOP")) == [0, None, False, ""]
