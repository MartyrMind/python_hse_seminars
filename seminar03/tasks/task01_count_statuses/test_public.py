from seminar03.tasks.task01_count_statuses.count_statuses import count_statuses


def test_counts_repeated_statuses() -> None:
    assert count_statuses(["new", "done", "new", "failed", "done", "new"]) == {
        "new": 3,
        "done": 2,
        "failed": 1,
    }


def test_preserves_order_of_first_appearance() -> None:
    assert list(count_statuses(["done", "new", "done", "failed"])) == [
        "done",
        "new",
        "failed",
    ]


def test_distinguishes_case_and_empty_status() -> None:
    assert count_statuses(["OK", "ok", "", "OK"]) == {"OK": 2, "ok": 1, "": 1}


def test_empty_input_produces_empty_dictionary() -> None:
    assert count_statuses([]) == {}


def test_does_not_change_input() -> None:
    statuses = ["new", "done", "new"]
    count_statuses(statuses)
    assert statuses == ["new", "done", "new"]
