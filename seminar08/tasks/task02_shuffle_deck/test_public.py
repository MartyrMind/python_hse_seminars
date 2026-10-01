from collections.abc import Iterator
from random import Random
from typing import Any

import pytest

from seminar08.tasks.task02_shuffle_deck.enable_shuffle import Deck, enable_shuffle


@pytest.fixture(autouse=True)
def restore_deck_class() -> Iterator[None]:
    original = Deck.__dict__.get("__setitem__")
    yield
    if original is None:
        if "__setitem__" in Deck.__dict__:
            delattr(Deck, "__setitem__")
    else:
        type.__setattr__(Deck, "__setitem__", original)


def test_unpatched_deck_does_not_support_item_assignment() -> None:
    deck: Any = Deck(["туз", "король"])

    assert "__setitem__" not in Deck.__dict__
    with pytest.raises(TypeError):
        deck[0] = "дама"


def test_patch_enables_assignment() -> None:
    deck: Any = Deck(["туз", "король", "дама"])

    enable_shuffle()
    deck[1] = "валет"

    assert list(deck) == ["туз", "валет", "дама"]


def test_assignment_keeps_list_index_rules() -> None:
    deck: Any = Deck(["туз", "король"])
    enable_shuffle()

    deck[-1] = "дама"
    assert list(deck) == ["туз", "дама"]
    with pytest.raises(IndexError):
        deck[2] = "валет"


def test_shuffle_matches_the_same_operation_on_a_list() -> None:
    cards = ["туз", "король", "дама", "валет", "десятка"]
    expected = cards.copy()
    Random(17).shuffle(expected)
    deck: Any = Deck(cards)

    enable_shuffle()
    Random(17).shuffle(deck)

    assert list(deck) == expected
    assert cards == ["туз", "король", "дама", "валет", "десятка"]


def test_patch_affects_existing_and_new_instances() -> None:
    old: Any = Deck(["туз", "король"])
    enable_shuffle()
    new: Any = Deck(["дама", "валет"])

    old[0] = "десятка"
    new[1] = "девятка"

    assert list(old) == ["десятка", "король"]
    assert list(new) == ["дама", "девятка"]
