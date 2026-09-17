from seminar04.tasks.task04_remove_exact.remove_exact import remove_exact


def test_removes_the_exact_object() -> None:
    target = {"name": "same"}
    items: list[object] = [target, "tail"]
    assert remove_exact(items, target) is True
    assert items == ["tail"]


def test_does_not_remove_equal_but_different_object() -> None:
    equal_copy = {"name": "same"}
    target = {"name": "same"}
    items: list[object] = [equal_copy, target]
    assert remove_exact(items, target) is True
    assert len(items) == 1
    assert items[0] is equal_copy


def test_returns_false_and_changes_nothing_when_object_is_absent() -> None:
    present = [1, 2]
    absent = [1, 2]
    items: list[object] = [present, "tail"]
    assert remove_exact(items, absent) is False
    assert len(items) == 2
    assert items[0] is present


def test_distinguishes_boolean_from_equal_integer() -> None:
    one = int("1")
    flag = True
    items: list[object] = [one, flag]
    assert one == flag
    assert remove_exact(items, flag) is True
    assert len(items) == 1
    assert items[0] is one


def test_can_remove_nan_by_identity() -> None:
    nan = float("nan")
    items: list[object] = [nan]
    assert nan != nan
    assert remove_exact(items, nan) is True
    assert items == []


def test_removes_only_first_occurrence_of_same_object() -> None:
    target: list[int] = []
    items: list[object] = [target, target, "tail"]
    assert remove_exact(items, target) is True
    assert len(items) == 2
    assert items[0] is target
    assert items[1] == "tail"
