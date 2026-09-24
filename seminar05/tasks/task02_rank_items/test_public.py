from typing import Any

from seminar05.tasks.task02_rank_items.rank_items import rank_items


def test_ranks_descending_and_keeps_ties_in_input_order() -> None:
    rows = [{"name": "B", "points": 3}, {"name": "A", "points": 3}, {"name": "C", "points": 8}]

    def points(row: dict[str, Any]) -> int:
        return int(row["points"])

    result = rank_items(rows, score=points)
    assert [row["name"] for row in result] == ["C", "B", "A"]
    assert result is not rows
    assert result[0] is rows[2]
    assert [row["name"] for row in rows] == ["B", "A", "C"]


def test_predicate_runs_once_per_item_before_scoring_kept_items() -> None:
    events: list[tuple[str, int]] = []

    def accept(value: int) -> bool:
        events.append(("accept", value))
        return value >= 0

    def score(value: int) -> int:
        events.append(("score", value))
        return value

    assert rank_items([3, -2, 0, 3], score=score, accept=accept) == [3, 3, 0]
    assert events == [
        ("accept", 3),
        ("accept", -2),
        ("accept", 0),
        ("accept", 3),
        ("score", 3),
        ("score", 0),
        ("score", 3),
    ]


def test_reverse_false_and_builtin_function_as_score() -> None:
    assert rank_items(["bbb", "a", "cc"], score=len, reverse=False) == ["a", "cc", "bbb"]


def test_zero_and_negative_scores_are_valid() -> None:
    def identity(value: int) -> int:
        return value

    assert rank_items([-5, 0, -1], score=identity) == [0, -1, -5]


def test_ascending_order_also_preserves_ties() -> None:
    assert rank_items(["bb", "aa", "c"], score=len, reverse=False) == ["c", "bb", "aa"]


def test_empty_or_rejected_input_does_not_call_score() -> None:
    def unexpected(value: Any) -> int:
        raise AssertionError("Для отсутствующего элемента score вызывать нельзя")

    def reject(value: int) -> bool:
        return False

    empty: list[Any] = []
    result = rank_items(empty, score=unexpected)
    assert result == []
    assert result is not empty
    assert rank_items([1, 2], score=unexpected, accept=reject) == []


def test_bound_method_can_be_used_as_score() -> None:
    class Rubric:
        def __init__(self, target: int) -> None:
            self.target = target

        def score(self, value: int) -> int:
            return -abs(value - self.target)

    rubric = Rubric(10)
    assert rank_items([2, 11, 9, 20], score=rubric.score) == [11, 9, 2, 20]
