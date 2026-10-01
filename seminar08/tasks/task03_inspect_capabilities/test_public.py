from collections.abc import Iterator
from typing import Any

import pytest

from seminar08.tasks.task03_inspect_capabilities.inspect_capabilities import (
    CapabilityReport,
    inspect_capabilities,
)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (42, CapabilityReport(False, False, False, True, True)),
        ([1, 2], CapabilityReport(True, True, True, False, False)),
        ((1, [2]), CapabilityReport(True, True, True, True, False)),
    ],
)
def test_standard_objects_show_abc_and_operation_results(
    value: Any, expected: CapabilityReport
) -> None:
    assert inspect_capabilities(value) == expected


def test_old_indexing_protocol_starts_iteration_without_iterable_abc() -> None:
    class LegacyShelf:
        def __getitem__(self, index: int) -> str:
            if index == 0:
                return "книга"
            raise IndexError

    assert inspect_capabilities(LegacyShelf()) == CapabilityReport(True, False, True, True, True)


def test_instance_only_special_method_fools_hasattr_but_not_iter() -> None:
    class Empty:
        pass

    value: Any = Empty()
    value.__getitem__ = lambda index: "книга"

    assert inspect_capabilities(value) == CapabilityReport(True, False, False, True, True)


def test_successful_iter_does_not_need_to_consume_elements() -> None:
    class DelayedFailure:
        def __iter__(self) -> Iterator[int]:
            return self

        def __next__(self) -> int:
            raise RuntimeError("ошибка при получении элемента")

    assert inspect_capabilities(DelayedFailure()) == CapabilityReport(
        False, True, True, True, True
    )


def test_unexpected_hash_error_propagates() -> None:
    error = ValueError("сломанный хеш")

    class BrokenHash:
        def __hash__(self) -> int:
            raise error

    with pytest.raises(ValueError) as caught:
        inspect_capabilities(BrokenHash())
    assert caught.value is error


def test_unexpected_iter_error_propagates() -> None:
    error = RuntimeError("сломанный итератор")

    class BrokenIterator:
        def __iter__(self) -> Iterator[int]:
            raise error

    with pytest.raises(RuntimeError) as caught:
        inspect_capabilities(BrokenIterator())
    assert caught.value is error
