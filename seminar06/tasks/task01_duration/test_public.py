from typing import Any

import pytest

from seminar06.tasks.task01_duration.duration import Duration


@pytest.mark.parametrize(("left", "right", "expected"), [(30, 90, 120), (0, 0, 0), (0, 5, 5)])
def test_addition_returns_duration_without_changing_operands(
    left: int, right: int, expected: int
) -> None:
    first: Any = Duration(left)
    second = Duration(right)
    result = first + second
    assert isinstance(result, Duration)
    assert result.seconds == expected
    assert (first.seconds, second.seconds) == (left, right)


@pytest.mark.parametrize(
    ("seconds", "expected"), [([30, 90, 30], 150), ([7], 7), ([0], 0), ([0, 4, 0], 4)]
)
def test_builtin_sum_returns_a_duration(seconds: list[int], expected: int) -> None:
    durations: list[Any] = [Duration(value) for value in seconds]
    result = sum(durations)
    assert isinstance(result, Duration)
    assert result.seconds == expected
    assert [item.seconds for item in durations] == seconds


def test_same_object_can_appear_several_times() -> None:
    part: Any = Duration(20)
    result = sum([part, part, part])
    assert isinstance(result, Duration)
    assert result.seconds == 60
    assert part.seconds == 20


def test_addition_can_be_chained() -> None:
    first: Any = Duration(1)
    result = first + Duration(2) + Duration(3)
    assert isinstance(result, Duration)
    assert result.seconds == 6
    assert first.seconds == 1
