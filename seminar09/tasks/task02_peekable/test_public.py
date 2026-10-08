from collections.abc import Iterator
from typing import Any

import pytest

from seminar09.tasks.task02_peekable.peekable import Peekable

pytestmark = pytest.mark.timeout(5)


def test_peek_buffers_exactly_one_value() -> None:
    seen: list[int] = []

    def source() -> Iterator[int]:
        for value in [10, 20, 30]:
            seen.append(value)
            yield value

    walk = Peekable(source())
    assert seen == []
    assert iter(walk) is walk
    assert walk.peek() == 10
    assert seen == [10]
    assert walk.peek() == 10
    assert next(walk) == 10
    assert seen == [10]
    assert next(walk) == 20
    assert seen == [10, 20]
    assert walk.peek() == 30
    assert list(walk) == [30]
    assert seen == [10, 20, 30]


def test_false_values_and_object_identity_are_preserved() -> None:
    token: list[int] = []
    walk: Peekable[Any] = Peekable([None, False, 0, "", token])
    for value in [None, False, 0, "", token]:
        assert walk.peek() is value
        assert walk.peek() is value
        assert next(walk) is value


def test_iterator_is_obtained_once_without_reading() -> None:
    events: list[str] = []

    class Source:
        def __iter__(self) -> Iterator[int]:
            events.append("iter")
            assert events == ["iter"]
            return iter([1, 2])

    walk = Peekable(Source())
    assert events == ["iter"]
    assert list(walk) == [1, 2]
    assert list(walk) == []
    assert events == ["iter"]


@pytest.mark.parametrize("first_method", ["peek", "next"])
def test_exhaustion_is_sticky(first_method: str) -> None:
    class RevivingSource:
        def __init__(self) -> None:
            self.calls = 0

        def __iter__(self) -> Iterator[int]:
            return self

        def __next__(self) -> int:
            self.calls += 1
            if self.calls == 1:
                raise StopIteration
            return 99

    source = RevivingSource()
    walk = Peekable(source)
    with pytest.raises(StopIteration):
        walk.peek() if first_method == "peek" else next(walk)
    for operation in [walk.peek, lambda: next(walk), walk.peek]:
        with pytest.raises(StopIteration):
            operation()
    assert source.calls == 1


@pytest.mark.parametrize("first_method", ["peek", "next"])
def test_unrelated_failure_does_not_exhaust_the_wrapper(first_method: str) -> None:
    failure = RuntimeError("попробуйте ещё раз")

    class RecoveringSource:
        def __init__(self) -> None:
            self.calls = 0

        def __iter__(self) -> Iterator[int]:
            return self

        def __next__(self) -> int:
            self.calls += 1
            if self.calls == 1:
                raise failure
            return 7

    source = RecoveringSource()
    walk = Peekable(source)
    with pytest.raises(RuntimeError) as caught:
        walk.peek() if first_method == "peek" else next(walk)
    assert caught.value is failure
    assert walk.peek() == 7
    assert next(walk) == 7
    assert source.calls == 2


def test_infinite_source_is_not_materialized() -> None:
    def source() -> Iterator[int]:
        number = 0
        while True:
            assert number < 3, "читать дальше пока не просили"
            yield number
            number += 1

    walk = Peekable(source())
    assert walk.peek() == 0
    assert next(walk) == 0
    assert next(walk) == 1
    assert walk.peek() == 2


def test_noniterable_source_raises_type_error() -> None:
    with pytest.raises(TypeError):
        Peekable(42)  # type: ignore[arg-type]
