from collections.abc import Iterator
from itertools import islice, repeat

import pytest

from seminar10.tasks.task02_window_counts.window_counts import window_counts

pytestmark = pytest.mark.timeout(5)


def test_window_evicts_old_values_and_removes_zero_counts() -> None:
    assert list(window_counts(iter(["a", "b", "a", "c", "c"]), 3)) == [
        {"a": 1}, {"a": 1, "b": 1}, {"a": 2, "b": 1},
        {"a": 1, "b": 1, "c": 1}, {"a": 1, "c": 2},
    ]


@pytest.mark.parametrize("width", [1, 2, 10])
def test_empty_source(width: int) -> None:
    assert list(window_counts([], width)) == []


def test_single_position_and_empty_strings() -> None:
    assert list(window_counts(["", "b", ""], 1)) == [{"": 1}, {"b": 1}, {"": 1}]


def test_snapshots_do_not_share_the_live_counter() -> None:
    walk = window_counts(["x", "y", "y"], 2)
    first = next(walk)
    assert type(first) is dict
    first["alien"] = 99
    second = next(walk)
    assert second == {"x": 1, "y": 1}
    assert next(walk) == {"y": 2}
    assert second == {"x": 1, "y": 1}


def test_source_is_started_lazily_and_read_once_per_result() -> None:
    events: list[str] = []

    class Source:
        def __iter__(self) -> Iterator[str]:
            assert events == [], "Повторный запуск источника"
            events.append("iter")
            return self.values()

        def values(self) -> Iterator[str]:
            for value in ("a", "b", "c"):
                events.append(value)
                yield value

    walk = window_counts(Source(), 2)
    assert events == []
    assert next(walk) == {"a": 1}
    assert events == ["iter", "a"]
    assert next(walk) == {"a": 1, "b": 1}
    assert events == ["iter", "a", "b"]


def test_infinite_source_can_be_consumed_partly() -> None:
    assert list(islice(window_counts(repeat("a"), 2), 4)) == [
        {"a": 1}, {"a": 2}, {"a": 2}, {"a": 2},
    ]


@pytest.mark.parametrize("width", [0, -1])
def test_invalid_width_does_not_start_source(width: int) -> None:
    class Source:
        def __iter__(self) -> Iterator[str]:
            raise AssertionError("Источник не должен запускаться")

    walk = window_counts(Source(), width)
    with pytest.raises(ValueError):
        next(walk)


def test_source_error_preserves_identity_and_previous_snapshot() -> None:
    failure = RuntimeError("нет данных")

    def source() -> Iterator[str]:
        yield "a"
        raise failure

    walk = window_counts(source(), 2)
    first = next(walk)
    with pytest.raises(RuntimeError) as caught:
        next(walk)
    assert caught.value is failure
    assert first == {"a": 1}
