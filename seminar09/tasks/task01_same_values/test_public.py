from collections.abc import Iterator
from typing import Any

import pytest

from seminar09.tasks.task01_same_values.same_values import same_values

pytestmark = pytest.mark.timeout(5)


@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [
        ([], [], True),
        ([1, None, False, ""], [1, None, False, ""], True),
        ([0], [False], True),
        ([1, 2], [1, 9], False),
        ([1], [1, 2], False),
        ([1, 2], [1], False),
        ([], [None], False),
        ([None], [], False),
    ],
)
def test_values_and_lengths(left: list[Any], right: list[Any], expected: bool) -> None:
    assert same_values(left, right) is expected


def test_one_shot_sources_are_not_restarted() -> None:
    class OneShot:
        def __init__(self) -> None:
            self.started = False

        def __iter__(self) -> Iterator[int]:
            assert not self.started, "источник нельзя запускать второй раз"
            self.started = True
            return iter([1, 2, 3])

    assert same_values(OneShot(), OneShot())


def test_mismatch_stops_without_reading_the_tail() -> None:
    events: list[str] = []

    def source(label: str, values: list[int]) -> Iterator[int]:
        for value in values:
            events.append(f"{label}:{value}")
            yield value
        raise AssertionError("после различия чтение запрещено")

    left = source("L", [1, 7])
    right = source("R", [1, 8])
    assert not same_values(left, right)
    assert events == ["L:1", "R:1", "L:7", "R:8"]


def test_length_mismatch_consumes_only_one_unmatched_value() -> None:
    right = iter([1, 2, 3])
    assert not same_values(iter([1]), right)
    assert next(right) == 3

    left = iter([1, 2, 3])
    assert not same_values(left, iter([1]))
    assert next(left) == 3


def test_current_positions_and_shared_iterator() -> None:
    left = iter([99, 1, 2])
    next(left)
    assert same_values(left, iter([1, 2]))
    shared = iter([1, 1, 2, 2])
    assert same_values(shared, shared)


def test_legacy_indexed_source_is_supported() -> None:
    class Legacy:
        def __getitem__(self, index: int) -> int:
            if index >= 2:
                raise IndexError(index)
            return index + 1

    assert same_values(Legacy(), iter([1, 2]))  # type: ignore[arg-type]


def test_reading_error_is_not_treated_as_end() -> None:
    failure = RuntimeError("источник сломан")

    def broken() -> Iterator[int]:
        yield 1
        raise failure

    with pytest.raises(RuntimeError) as caught:
        same_values(broken(), iter([1, 2]))
    assert caught.value is failure


def test_equality_error_propagates() -> None:
    failure = ValueError("сравнение сломано")

    class BrokenEquality:
        def __eq__(self, other: object) -> bool:
            raise failure

    with pytest.raises(ValueError) as caught:
        same_values([BrokenEquality()], [0])
    assert caught.value is failure


def test_equality_is_not_replaced_by_a_custom_ne() -> None:
    class ContradictoryEquality:
        def __eq__(self, other: object) -> bool:
            return False

        def __ne__(self, other: object) -> bool:
            return False

    assert not same_values([ContradictoryEquality()], [0])


def test_error_obtaining_an_iterator_propagates() -> None:
    failure = RuntimeError("обход недоступен")

    class Unavailable:
        def __iter__(self) -> Iterator[int]:
            raise failure

    with pytest.raises(RuntimeError) as caught:
        same_values(Unavailable(), [])
    assert caught.value is failure


def test_infinite_inputs_can_differ_after_a_finite_prefix() -> None:
    def increasing() -> Iterator[int]:
        number = 0
        while True:
            assert number < 5, "после первого различия источник читать нельзя"
            yield number
            number += 1

    assert not same_values(increasing(), iter([0, 1, -1]))
