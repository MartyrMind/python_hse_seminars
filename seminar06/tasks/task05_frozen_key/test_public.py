import pytest

from seminar06.tasks.task05_frozen_key.frozen_key import Data, FrozenKey


@pytest.mark.parametrize("data", [0, -3, "", "hello", [], {}, [1, "a"], {"x": [1]}])
def test_equal_data_produce_equal_hashable_keys(data: Data) -> None:
    left, right = FrozenKey(data), FrozenKey(data)
    assert left is not right
    assert left == right
    assert hash(left) == hash(right)
    assert {left: "found"}[right] == "found"
    assert len({left, right}) == 1


def test_dictionary_order_is_ignored_at_every_depth() -> None:
    left = FrozenKey({"a": [{"x": 1, "y": 2}], "b": 3})
    right = FrozenKey({"b": 3, "a": [{"y": 2, "x": 1}]})
    assert left == right
    assert hash(left) == hash(right)
    assert {left: "found"}[right] == "found"


@pytest.mark.parametrize(
    ("left", "right"),
    [
        ([1, 2], [2, 1]),
        ([], {}),
        (1, "1"),
        (-1, -2),
        ({"a": 1}, [["a", 1]]),
        ({"a": [1]}, {"a": [2]}),
        ({"a": 1}, {"b": 1}),
        ([1], [1, 1]),
    ],
)
def test_different_contents_and_container_types_stay_distinct(left: Data, right: Data) -> None:
    first, second = FrozenKey(left), FrozenKey(right)
    assert first != second
    assert len({first, second}) == 2


def test_original_mutations_do_not_change_key_hash_or_lookup() -> None:
    scores: list[Data] = [3, 5]
    data: dict[str, Data] = {"scores": scores, "name": "Аня"}
    key = FrozenKey(data)
    before = hash(key)
    results = {key: "готово"}
    scores.append(9)
    data["name"] = "Борис"
    data["new"] = 1
    assert hash(key) == before
    assert results[key] == "готово"
    assert results[FrozenKey({"name": "Аня", "scores": [3, 5]})] == "готово"
    assert key != FrozenKey(data)


def test_shared_inner_objects_are_compared_by_contents() -> None:
    shared: list[Data] = [1, {"x": 2}]
    key = FrozenKey([shared, shared])
    independent = FrozenKey([[1, {"x": 2}], [1, {"x": 2}]])
    assert key == independent
    assert hash(key) == hash(independent)
    shared.clear()
    assert key == independent
    assert len({key, independent}) == 1


def test_construction_does_not_modify_input() -> None:
    data: dict[str, Data] = {"b": [2, 1], "a": {"x": 3}}
    FrozenKey(data)
    assert data == {"b": [2, 1], "a": {"x": 3}}
    assert list(data) == ["b", "a"]


def test_separate_snapshots_of_one_object_capture_different_states() -> None:
    data: list[Data] = [1]
    before = FrozenKey(data)
    data.append(2)
    after = FrozenKey(data)
    assert before == FrozenKey([1])
    assert after == FrozenKey([1, 2])
    assert len({before, after}) == 2
