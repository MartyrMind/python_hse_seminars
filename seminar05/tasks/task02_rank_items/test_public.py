from collections.abc import Callable
from typing import Any

from seminar05.tasks.task02_rank_items.rank_items import rank_items


def points(row: dict[str, Any]) -> int:
    return int(row["points"])


def attempts(row: dict[str, Any]) -> int:
    return int(row["attempts"])


def test_primary_criterion_takes_precedence_over_secondary() -> None:
    rows = [
        {"name": "A", "points": 8, "attempts": 1},
        {"name": "B", "points": 10, "attempts": 3},
        {"name": "C", "points": 10, "attempts": 1},
        {"name": "D", "points": 8, "attempts": 2},
    ]
    criteria: list[tuple[Callable[[Any], int], bool]] = [(points, True), (attempts, False)]
    result = rank_items(rows, criteria=criteria)
    assert [row["name"] for row in result] == ["C", "B", "A", "D"]
    assert result is not rows
    assert result[0] is rows[2]
    assert [row["name"] for row in rows] == ["A", "B", "C", "D"]
    assert criteria == [(points, True), (attempts, False)]


def test_three_criteria_with_independent_directions_and_complete_ties() -> None:
    rows = [(1, 2, 3, "A"), (1, 2, 3, "B"), (1, 2, 1, "C"), (1, 3, 9, "D"), (0, 0, 0, "E")]

    def first(row: tuple[int, int, int, str]) -> int:
        return row[0]

    def second(row: tuple[int, int, int, str]) -> int:
        return row[1]

    def third(row: tuple[int, int, int, str]) -> int:
        return row[2]

    result = rank_items(rows, criteria=[(first, False), (second, True), (third, False)])
    assert [row[3] for row in result] == ["E", "D", "C", "A", "B"]


def test_filter_finishes_before_scoring_and_each_criterion_runs_once_per_kept_occurrence() -> None:
    events: list[tuple[str, int]] = []

    def accept(value: int) -> bool:
        events.append(("accept", value))
        return value >= 0

    def first(value: int) -> int:
        events.append(("first", value))
        return value % 2

    def second(value: int) -> int:
        events.append(("second", value))
        return value

    assert rank_items([3, -2, 0, 3], criteria=[(first, False), (second, True)], accept=accept) == [
        0,
        3,
        3,
    ]
    assert events[:4] == [("accept", 3), ("accept", -2), ("accept", 0), ("accept", 3)]
    assert sorted(events[4:]) == sorted(
        [
            ("first", 3),
            ("first", 0),
            ("first", 3),
            ("second", 3),
            ("second", 0),
            ("second", 3),
        ]
    )


def test_one_criterion_accepts_builtin_function_and_preserves_ties() -> None:
    assert rank_items(["bb", "aa", "c"], criteria=[(len, False)]) == ["c", "bb", "aa"]
    assert rank_items(["c", "bb", "aa"], criteria=[(len, True)]) == ["bb", "aa", "c"]


def test_empty_criteria_still_filters_without_changing_order() -> None:
    def positive(value: int) -> bool:
        return value > 0

    values = [3, -1, 2]
    assert rank_items(values, criteria=[], accept=positive) == [3, 2]
    result = rank_items(values, criteria=[])
    assert result == values and result is not values


def test_empty_or_rejected_input_does_not_call_criteria() -> None:
    def unexpected(value: Any) -> int:
        raise AssertionError("Для отсутствующего элемента критерий вызывать нельзя")

    def reject(value: int) -> bool:
        return False

    empty: list[Any] = []
    result = rank_items(empty, criteria=[(unexpected, True)])
    assert result == [] and result is not empty
    assert rank_items([1, 2], criteria=[(unexpected, True)], accept=reject) == []


def test_bound_method_and_negative_scores() -> None:
    class Rubric:
        def __init__(self, target: int) -> None:
            self.target = target

        def score(self, value: int) -> int:
            return -abs(value - self.target)

    rubric = Rubric(10)
    assert rank_items([2, 11, 9, 20], criteria=[(rubric.score, True)]) == [11, 9, 2, 20]
