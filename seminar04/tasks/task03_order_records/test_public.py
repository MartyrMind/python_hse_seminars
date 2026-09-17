from collections.abc import Callable

from seminar04.tasks.task03_order_records.order_records import (
    Record,
    order_records_in_place,
    ordered_records,
)


def names(records: list[Record]) -> list[str]:
    return [record["name"] for record in records]


def sample() -> list[Record]:
    return [
        {"group": "B", "score": 8, "name": "Борис"},
        {"group": "A", "score": 7, "name": "Анна"},
        {"group": "A", "score": 10, "name": "Вера"},
        {"group": "A", "score": 10, "name": "Глеб"},
        {"group": "B", "score": 9, "name": "Дина"},
    ]


def test_orders_by_group_then_score_descending() -> None:
    assert names(ordered_records(sample())) == ["Вера", "Глеб", "Анна", "Дина", "Борис"]


def test_equal_group_and_score_keep_original_order() -> None:
    records: list[Record] = [
        {"group": "A", "score": 10, "name": "second alphabetically"},
        {"group": "A", "score": 10, "name": "first alphabetically"},
    ]
    assert names(ordered_records(records)) == ["second alphabetically", "first alphabetically"]


def test_ordered_records_returns_new_list_without_copying_records() -> None:
    records = sample()
    result = ordered_records(records)
    assert result is not records
    assert names(records) == ["Борис", "Анна", "Вера", "Глеб", "Дина"]
    assert {id(record) for record in result} == {id(record) for record in records}


def test_in_place_version_changes_same_list_and_returns_none() -> None:
    records = sample()
    alias = records
    operation: Callable[[list[Record]], object] = order_records_in_place
    result = operation(records)
    assert result is None
    assert alias is records
    assert names(alias) == ["Вера", "Глеб", "Анна", "Дина", "Борис"]


def test_empty_and_single_record_lists() -> None:
    empty: list[Record] = []
    assert ordered_records(empty) == []
    order_records_in_place(empty)
    assert empty == []

    one: list[Record] = [{"group": "A", "score": 1, "name": "Анна"}]
    result = ordered_records(one)
    assert result == one
    assert result is not one
