from collections.abc import Callable

from seminar04.tasks.task01_replace_contents.replace_contents import replace_contents


def test_replaces_all_values() -> None:
    target = [1, 2, 3]
    operation: Callable[[list[int], list[int]], object] = replace_contents
    result = operation(target, [8, 9])
    assert result is None
    assert target == [8, 9]


def test_alias_observes_replacement() -> None:
    target = [1, 2, 3]
    alias = target
    replace_contents(target, [4, 5])
    assert alias == [4, 5]
    assert alias is target


def test_can_replace_with_empty_list() -> None:
    target = [1, 2]
    replace_contents(target, [])
    assert target == []


def test_can_fill_an_empty_list() -> None:
    target: list[int] = []
    replace_contents(target, [1, 2])
    assert target == [1, 2]


def test_replacement_is_unchanged() -> None:
    target = [1]
    replacement = [2, 3]
    replace_contents(target, replacement)
    assert replacement == [2, 3]


def test_replacing_list_with_itself_is_supported() -> None:
    target = [1, 2, 3]
    replace_contents(target, target)
    assert target == [1, 2, 3]
