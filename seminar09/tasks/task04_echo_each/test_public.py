import inspect
from collections.abc import Iterator
from typing import Any

import pytest

from seminar09.tasks.task04_echo_each.echo_each import echo_each

pytestmark = pytest.mark.timeout(5)


@pytest.mark.parametrize(
    ("values", "expected"),
    [([], []), ([1], [1, 1]), ([1, 2], [1, 1, 2, 2]), ([None, 0], [None, None, 0, 0])],
)
def test_each_value_is_repeated_twice(values: list[Any], expected: list[Any]) -> None:
    walk = echo_each(iter(values))
    assert inspect.isgenerator(walk)
    assert iter(walk) is walk
    assert list(walk) == expected
    assert list(walk) == []


def test_creation_does_not_even_obtain_the_source_iterator() -> None:
    events: list[str] = []

    class Source:
        def __iter__(self) -> Iterator[int]:
            events.append("iter")
            return iter([7])

    walk = echo_each(Source())
    assert events == []
    assert next(walk) == 7
    assert events == ["iter"]


def test_source_progress_is_visible_after_every_next() -> None:
    seen: list[int] = []

    def source() -> Iterator[int]:
        for value in [10, 20]:
            seen.append(value)
            yield value
        seen.append(99)

    walk = echo_each(source())
    assert seen == []
    assert next(walk) == 10
    assert seen == [10]
    assert next(walk) == 10
    assert seen == [10]
    assert next(walk) == 20
    assert seen == [10, 20]
    assert next(walk) == 20
    assert seen == [10, 20]
    with pytest.raises(StopIteration):
        next(walk)
    assert seen == [10, 20, 99]


def test_source_iterator_is_requested_only_once() -> None:
    class OneShot:
        def __init__(self) -> None:
            self.started = False

        def __iter__(self) -> Iterator[int]:
            assert not self.started, "нельзя обходить источник повторно"
            self.started = True
            return iter([1, 2])

    assert list(echo_each(OneShot())) == [1, 1, 2, 2]


def test_mutable_elements_are_not_copied() -> None:
    token: list[int] = []
    walk = echo_each([token])
    assert next(walk) is token
    token.append(5)
    assert next(walk) is token


def test_infinite_input_is_consumed_only_on_demand() -> None:
    def source() -> Iterator[int]:
        number = 0
        while True:
            assert number < 3, "лишнее чтение"
            yield number
            number += 1

    walk = echo_each(source())
    assert [next(walk) for _ in range(5)] == [0, 0, 1, 1, 2]


def test_error_appears_after_both_copies_of_the_previous_value() -> None:
    failure = RuntimeError("источник сломался")

    def source() -> Iterator[int]:
        yield 7
        raise failure

    walk = echo_each(source())
    assert next(walk) == 7
    assert next(walk) == 7
    with pytest.raises(RuntimeError) as caught:
        next(walk)
    assert caught.value is failure
    with pytest.raises(StopIteration):
        next(walk)
