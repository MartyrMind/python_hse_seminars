from typing import Any

import pytest

from seminar08.tasks.task05_card_sources.card_sources import CardSource, QueueSource, StackSource

card_source_type: Any = CardSource
stack_type: Any = StackSource
queue_type: Any = QueueSource


def test_abstract_base_and_incomplete_child_cannot_be_instantiated() -> None:
    class Incomplete(CardSource):
        def put(self, card: str) -> None:
            pass

        def draw(self) -> str:
            return "A"

    incomplete_type: Any = Incomplete

    with pytest.raises(TypeError):
        card_source_type()
    with pytest.raises(TypeError):
        incomplete_type()


@pytest.mark.parametrize(
    ("source_type", "expected"),
    [(stack_type, ["C", "B", "A"]), (queue_type, ["A", "B", "C"])],
)
def test_sources_draw_in_different_orders(source_type: Any, expected: list[str]) -> None:
    source: Any = source_type(["A", "B", "C"])

    assert len(source) == 3
    assert source.draw_many(3) == expected
    assert source.is_empty()


@pytest.mark.parametrize(
    ("source_type", "first"), [(stack_type, "C"), (queue_type, "A")]
)
def test_load_accepts_generator_and_source_is_callable(source_type: Any, first: str) -> None:
    source: Any = source_type()
    source.load(card for card in ["A", "B", "C"])

    assert callable(source)
    assert source() == first
    assert len(source) == 2


@pytest.mark.parametrize("source_type", [stack_type, queue_type])
def test_draw_many_rejects_invalid_count_before_mutation(source_type: Any) -> None:
    source: Any = source_type(["A", "B"])

    with pytest.raises(ValueError):
        source.draw_many(-1)
    with pytest.raises(LookupError):
        source.draw_many(3)

    assert len(source) == 2
    assert source.draw_many(0) == []
    assert len(source) == 2


@pytest.mark.parametrize("source_type", [stack_type, queue_type])
def test_draw_from_empty_source_raises_lookup_error(source_type: Any) -> None:
    source: Any = source_type()

    assert source.is_empty()
    with pytest.raises(LookupError):
        source.draw()


def test_shared_methods_work_with_a_third_storage_layout() -> None:
    class ThirdPartySource(CardSource):
        def __init__(self) -> None:
            self.entries: list[str] = []

        def put(self, card: str) -> None:
            self.entries.append(card)

        def draw(self) -> str:
            if not self.entries:
                raise LookupError("empty source")
            return self.entries.pop(0)

        def __len__(self) -> int:
            return len(self.entries)

    source: Any = ThirdPartySource()
    source.load(["A", "B", "C"])

    assert not source.is_empty()
    assert source.draw_many(2) == ["A", "B"]
    assert source() == "C"
    assert source.is_empty()


def test_shared_methods_are_inherited_from_the_base() -> None:
    shared = {"load", "is_empty", "draw_many", "__call__"}

    assert shared <= CardSource.__dict__.keys()
    assert not shared.intersection(StackSource.__dict__)
    assert not shared.intersection(QueueSource.__dict__)
