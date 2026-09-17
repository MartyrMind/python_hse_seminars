from seminar03.tasks.task06_changes.changes import Config, changes


def test_reports_added_removed_and_changed_keys() -> None:
    before: Config = {"timeout": 30, "cache": "on", "retries": 3}
    after: Config = {"timeout": 45, "proxy": None, "retries": 3}
    assert changes(before, after) == {
        "cache": "removed",
        "proxy": "added",
        "timeout": "changed",
    }


def test_unchanged_keys_are_absent() -> None:
    assert changes({"a": 1, "b": "same"}, {"a": 1, "b": "same"}) == {}


def test_changing_only_the_type_is_a_change() -> None:
    assert changes({"mode": 1}, {"mode": True}) == {"mode": "changed"}
    assert changes({"ratio": 1}, {"ratio": 1.0}) == {"ratio": "changed"}


def test_none_is_a_value_not_an_absence() -> None:
    assert changes({"proxy": None}, {"proxy": None}) == {}
    assert changes({"proxy": None}, {}) == {"proxy": "removed"}
    assert changes({}, {"proxy": None}) == {"proxy": "added"}


def test_nan_is_always_changed() -> None:
    nan = float("nan")
    assert changes({"ratio": nan}, {"ratio": nan}) == {"ratio": "changed"}


def test_result_keys_are_alphabetical() -> None:
    before: Config = {"я": 1, "б": 1, "а": 1}
    after: Config = {"я": 2, "б": 2, "в": 2}
    assert list(changes(before, after)) == ["а", "б", "в", "я"]


def test_arguments_are_unchanged() -> None:
    before: Config = {"timeout": 30, "nested": [1, 2]}
    after: Config = {"timeout": 45, "nested": [1, 2]}
    changes(before, after)
    assert before == {"timeout": 30, "nested": [1, 2]}
    assert after == {"timeout": 45, "nested": [1, 2]}
