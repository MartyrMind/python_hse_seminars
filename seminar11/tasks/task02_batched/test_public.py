from collections.abc import Callable, Iterator
from inspect import unwrap
from typing import Any

import pytest

from seminar11.tasks.task02_batched.batched import batched

pytestmark = pytest.mark.timeout(5)


@pytest.mark.parametrize(
    ("size", "expected_batches"),
    [
        (1, [[10], [20], [30], [40], [50]]),
        (2, [[10, 20], [30, 40], [50]]),
        (3, [[10, 20, 30], [40, 50]]),
        (10, [[10, 20, 30, 40, 50]]),
    ],
)
def test_batches_preserve_order_and_forward_options(
    size: int, expected_batches: list[list[int]]
) -> None:
    calls: list[tuple[list[int], str]] = []

    @batched(size=size)
    def load(ids: list[int], /, *, currency: str = "RUB") -> list[str]:
        calls.append((ids, currency))
        return [f"{number}:{currency}" for number in ids]

    assert calls == []
    assert load([10, 20, 30, 40, 50], currency="EUR") == [
        "10:EUR",
        "20:EUR",
        "30:EUR",
        "40:EUR",
        "50:EUR",
    ]
    assert calls == [(batch, "EUR") for batch in expected_batches]


def test_source_is_read_once_and_only_current_batch_is_read_ahead() -> None:
    events: list[object] = []

    class Source:
        def __iter__(self) -> Iterator[int]:
            events.append("iter")
            assert events.count("iter") == 1
            return self.values()

        def values(self) -> Iterator[int]:
            for number in range(5):
                events.append(number)
                yield number

    @batched(2)
    def process(rows: list[int]) -> list[int]:
        events.append(tuple(rows))
        return rows

    assert events == []
    assert process(Source()) == [0, 1, 2, 3, 4]
    assert events == ["iter", 0, 1, (0, 1), 2, 3, (2, 3), 4, (4,)]


def test_empty_source_does_not_call_function() -> None:
    @batched(3)
    def forbidden(rows: list[int]) -> list[int]:
        raise AssertionError("пустой пакет передавать нельзя")

    assert forbidden(iter(())) == []


def test_batch_lists_are_fresh_and_items_and_options_are_not_copied() -> None:
    first, second, third = object(), object(), object()
    source = [first, second, third]
    batches: list[list[object]] = []
    option: list[int] = []

    @batched(2)
    def process(rows: list[object], options: list[int]) -> list[object]:
        assert options is option
        batches.append(rows)
        result = rows.copy()
        rows.clear()
        return result

    result = process(source, option)
    assert len(result) == 3
    assert all(left is right for left, right in zip(result, source, strict=True))
    assert source == [first, second, third]
    assert len(batches) == 2
    assert batches[0] is not batches[1]


def test_output_length_need_not_match_input_and_keyword_names_do_not_collide() -> None:
    @batched(2)
    def process(rows: list[int], /, *, items: str) -> list[str]:
        return [items] if len(rows) == 1 else []

    assert process([1, 2, 3], items="остаток") == ["остаток"]


def test_failure_does_not_read_next_batch_and_keeps_exception_identity() -> None:
    source = iter(range(10))
    error = LookupError("пакет отклонён")
    completed: list[int] = []

    @batched(2)
    def process(rows: list[int]) -> list[int]:
        if rows[0] == 2:
            raise error
        completed.extend(rows)
        return rows

    with pytest.raises(LookupError) as caught:
        process(source)
    assert caught.value is error
    assert completed == [0, 1]
    assert next(source) == 4


def test_source_failure_is_not_treated_as_a_partial_batch() -> None:
    error = RuntimeError("источник сломался")
    batches: list[list[int]] = []

    def source() -> Iterator[int]:
        yield 1
        yield 2
        yield 3
        raise error

    @batched(2)
    def process(rows: list[int]) -> list[int]:
        batches.append(rows)
        return rows

    with pytest.raises(RuntimeError) as caught:
        process(source())
    assert caught.value is error
    assert batches == [[1, 2]]


@pytest.mark.parametrize("size", [0, -1, -20])
def test_size_is_checked_at_factory_call(size: int) -> None:
    with pytest.raises(ValueError):
        batched(size)


def test_factory_can_be_reused_and_metadata_are_preserved() -> None:
    decorate = batched(2)

    def first(rows: list[int]) -> list[int]:
        """Первый обработчик."""
        return [sum(rows)]

    def second(rows: list[str]) -> list[str]:
        return ["".join(rows)]

    wrapped = decorate(first)
    other = decorate(second)
    assert wrapped.__name__ == "first"
    assert wrapped.__doc__ == "Первый обработчик."
    assert unwrap(wrapped) is first
    assert wrapped([1, 2, 3]) == [3, 3]
    assert other("abc") == ["ab", "c"]
    assert wrapped([4]) == [4]


@pytest.mark.parametrize("layers", [1, 2])
def test_wraps_preserves_full_metadata_at_each_layer(
    layers: int, assert_metadata: Callable[[Any, Any], None]
) -> None:
    def load[T](rows: list[T], /, *, label: str = "price") -> list[T]:
        """Загрузить цены."""
        return rows

    load.__dict__["audit_tag"] = object()
    wrapped: Any = load
    for _ in range(layers):
        original = wrapped
        wrapped = batched(2)(original)
        assert_metadata(wrapped, original)

    assert wrapped(iter([1, 2, 3]), label="EUR") == [1, 2, 3]
