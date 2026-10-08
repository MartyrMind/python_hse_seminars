from collections import OrderedDict
from collections.abc import Iterator

import pytest

from seminar10.tasks.task03_coalesce_updates.coalesce_updates import coalesce_updates

pytestmark = pytest.mark.timeout(5)


def test_values_and_order_follow_the_last_update() -> None:
    result = coalesce_updates([("x", 1), ("y", 2), ("x", 3), ("z", 4), ("y", 5)])
    assert isinstance(result, OrderedDict)
    assert list(result.items()) == [("x", 3), ("z", 4), ("y", 5)]


def test_repeating_the_same_value_still_moves_the_key() -> None:
    result = coalesce_updates([("x", 1), ("y", 2), ("x", 1)])
    assert list(result.items()) == [("y", 2), ("x", 1)]
    assert result.popitem(last=False) == ("y", 2)


def test_empty_input_and_independent_results() -> None:
    first: OrderedDict[str, int] = coalesce_updates([])
    second: OrderedDict[str, int] = coalesce_updates([])
    assert isinstance(first, OrderedDict)
    assert list(first.items()) == []
    first["x"] = 1
    assert second == {}


def test_one_shot_input_is_not_restarted() -> None:
    class Source:
        def __init__(self) -> None:
            self.started = False

        def __iter__(self) -> Iterator[tuple[str, int]]:
            if self.started:
                raise AssertionError("Повторный обход")
            self.started = True
            return iter([("a", 0), ("b", 2), ("a", 3)])

    assert list(coalesce_updates(Source()).items()) == [("b", 2), ("a", 3)]


def test_input_and_payload_identity_are_preserved() -> None:
    old: list[int] = []
    new = [2]
    updates = [("", old), ("x", old), ("", new)]
    result = coalesce_updates(updates)
    assert list(result) == ["x", ""]
    assert result[""] is new
    assert result["x"] is old
    assert updates == [("", []), ("x", []), ("", [2])]


def test_source_error_is_not_swallowed() -> None:
    failure = LookupError("потеря связи")

    def updates() -> Iterator[tuple[str, int]]:
        yield "x", 1
        raise failure

    with pytest.raises(LookupError) as caught:
        coalesce_updates(updates())
    assert caught.value is failure
