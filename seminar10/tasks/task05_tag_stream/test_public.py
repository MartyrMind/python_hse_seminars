from collections.abc import Iterator
from itertools import count, islice, repeat

import pytest

from seminar10.tasks.task05_tag_stream.tag_stream import tag_stream

pytestmark = pytest.mark.timeout(5)


def test_numbering_and_labels_continue_across_batch_boundaries() -> None:
    result = list(tag_stream([[10, 20], [], [30, 40]], ("a", "b", "c"), 10, start=-1))
    assert result == [(-1, "a", 10), (0, "b", 20), (1, "c", 30), (2, "a", 40)]
    assert result[0].number == -1
    assert result[0].label == "a"
    assert result[0].value == 10


def test_empty_labels_use_empty_string_forever() -> None:
    assert list(tag_stream([[1, 2, 3]], (), 3)) == [(1, "", 1), (2, "", 2), (3, "", 3)]


@pytest.mark.parametrize("limit", [0, -1])
def test_zero_and_invalid_limit_do_not_start_outer_source(limit: int) -> None:
    class Source:
        def __iter__(self) -> Iterator[list[int]]:
            raise AssertionError("Лишний запуск источника")

    walk = tag_stream(Source(), (), limit)
    if limit < 0:
        with pytest.raises(ValueError):
            next(walk)
    else:
        assert list(walk) == []


def test_no_eager_start_or_read_ahead_in_either_level() -> None:
    events: list[str] = []

    class Batch:
        def __init__(self, name: str, values: list[int]) -> None:
            self.name = name
            self.values = values

        def __iter__(self) -> Iterator[int]:
            events.append(self.name)
            return self.values_iterator()

        def values_iterator(self) -> Iterator[int]:
            for value in self.values:
                events.append(str(value))
                yield value

    class Source:
        def __iter__(self) -> Iterator[Batch]:
            events.append("outer")
            return self.batches()

        def batches(self) -> Iterator[Batch]:
            yield Batch("first", [10, 20])
            events.append("next batch")
            yield Batch("second", [30])

    walk = tag_stream(Source(), ("x",), 2)
    assert events == []
    assert next(walk) == (1, "x", 10)
    assert events == ["outer", "first", "10"]
    assert next(walk) == (2, "x", 20)
    assert events == ["outer", "first", "10", "20"]
    with pytest.raises(StopIteration):
        next(walk)
    assert events == ["outer", "first", "10", "20"]


def test_limit_does_not_consume_the_next_item() -> None:
    inner = iter([10, 20, 30])
    outer = iter([inner, [40]])
    assert list(tag_stream(outer, ("a",), 2)) == [(1, "a", 10), (2, "a", 20)]
    assert next(inner) == 30
    assert next(outer) == [40]


def test_infinite_inner_and_outer_sources() -> None:
    assert list(tag_stream([count()], ("a", "b"), 3)) == [
        (1, "a", 0), (2, "b", 1), (3, "a", 2),
    ]
    assert list(tag_stream(repeat([7]), (), 3)) == [(1, "", 7), (2, "", 7), (3, "", 7)]
    assert list(islice(tag_stream([count()], (), 100), 2)) == [(1, "", 0), (2, "", 1)]


def test_empty_batches_do_not_advance_labels_or_numbers() -> None:
    assert list(tag_stream([[], [], [5], [], [6]], ("a", "b"), 4)) == [
        (1, "a", 5), (2, "b", 6),
    ]
    assert list(tag_stream([[], []], ("a",), 4)) == []


def test_payloads_are_preserved_by_identity() -> None:
    payload: list[int] = []
    result = list(tag_stream([[payload]], (), 1))
    assert result[0].value is payload


def test_source_error_reaches_consumer_when_next_item_is_requested() -> None:
    failure = RuntimeError("сбой пакета")

    def batch() -> Iterator[int]:
        yield 1
        raise failure

    walk = tag_stream([batch()], (), 3)
    assert next(walk) == (1, "", 1)
    with pytest.raises(RuntimeError) as caught:
        next(walk)
    assert caught.value is failure


def test_outer_source_error_is_not_hidden() -> None:
    failure = LookupError("сбой получения пакета")

    def batches() -> Iterator[list[int]]:
        yield []
        yield [5]
        raise failure

    walk = tag_stream(batches(), (), 3)
    assert next(walk) == (1, "", 5)
    with pytest.raises(LookupError) as caught:
        next(walk)
    assert caught.value is failure
