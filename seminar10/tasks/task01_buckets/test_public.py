import pytest

from seminar10.tasks.task01_buckets.buckets import Buckets

pytestmark = pytest.mark.timeout(5)


def test_missing_peek_does_not_create_a_bucket() -> None:
    buckets = Buckets[int]()
    missing = buckets.peek("нет")
    assert missing == []
    missing.append(99)
    assert buckets.peek("нет") == []
    assert buckets.keys() == []
    buckets.add("есть", 0)
    assert buckets.peek("нет") == []
    assert buckets.keys() == ["есть"]


def test_buckets_keep_separate_lists_and_first_insertion_order() -> None:
    buckets = Buckets[int]()
    buckets.add("b", 1)
    buckets.add("a", 2)
    buckets.add("b", 3)
    assert buckets.peek("b") == [1, 3]
    assert buckets.peek("a") == [2]
    assert buckets.keys() == ["b", "a"]


def test_snapshots_are_independent_but_values_are_not_copied() -> None:
    buckets = Buckets[list[int]]()
    value = [1]
    buckets.add("x", value)
    snapshot = buckets.peek("x")
    assert snapshot[0] is value
    snapshot.clear()
    assert buckets.peek("x") == [[1]]
    old = buckets.peek("x")
    buckets.add("x", [2])
    assert old == [[1]]
    value.append(3)
    assert old == [[1, 3]]
    keys = buckets.keys()
    keys.clear()
    assert buckets.keys() == ["x"]


def test_empty_key_false_values_and_independent_instances() -> None:
    left = Buckets[object]()
    right = Buckets[object]()
    for item in (None, False, 0, ""):
        left.add("", item)
    assert left.peek("") == [None, False, 0, ""]
    assert left.keys() == [""]
    assert right.peek("") == []
    assert right.keys() == []
