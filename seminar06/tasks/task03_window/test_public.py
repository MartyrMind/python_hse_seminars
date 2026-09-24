from collections.abc import Callable

import pytest

from seminar06.tasks.task03_window.window import Window


@pytest.mark.parametrize(
    ("start", "stop", "length"), [(10, 20, 10), (0, 0, 0), (-7, -2, 5), (-3, 4, 7)]
)
def test_constructs_valid_interval(start: int, stop: int, length: int) -> None:
    window = Window(start, stop)
    assert (window.start, window.stop, window.length) == (start, stop, length)


@pytest.mark.parametrize(("start", "stop"), [(1, 0), (-2, -3), (20, 10)])
def test_rejects_reversed_boundaries_in_constructor(start: int, stop: int) -> None:
    with pytest.raises(ValueError):
        Window(start, stop)


def test_properties_update_length_and_allow_equal_boundaries() -> None:
    window = Window(10, 20)
    window.start = 15
    assert (window.start, window.stop, window.length) == (15, 20, 5)
    window.stop = 30
    assert window.length == 15
    window.start = 30
    assert window.length == 0
    window.start = -10
    window.stop = -10
    assert (window.start, window.stop, window.length) == (-10, -10, 0)


@pytest.mark.parametrize(("field", "value"), [("start", 21), ("stop", 9)])
def test_rejected_write_preserves_whole_state(field: str, value: int) -> None:
    window = Window(10, 20)
    with pytest.raises(ValueError):
        setattr(window, field, value)
    assert (window.start, window.stop, window.length) == (10, 20, 10)


def test_length_is_read_only() -> None:
    window = Window(10, 20)
    with pytest.raises(AttributeError):
        window.length = 99
    assert window.length == 10


@pytest.mark.parametrize(
    ("delta", "start", "stop"), [(100, 110, 120), (-100, -90, -80), (0, 10, 20)]
)
def test_move_preserves_length_and_instance(delta: int, start: int, stop: int) -> None:
    window = Window(10, 20)
    alias = window
    operation: Callable[[int], object] = window.move
    result = operation(delta)
    assert result is None
    assert alias is window
    assert (alias.start, alias.stop, alias.length) == (start, stop, 10)


def test_empty_interval_can_move_in_both_directions() -> None:
    window = Window(0, 0)
    window.move(100)
    assert (window.start, window.stop, window.length) == (100, 100, 0)
    window.move(-200)
    assert (window.start, window.stop, window.length) == (-100, -100, 0)


def test_windows_have_independent_state() -> None:
    first, second = Window(1, 3), Window(1, 3)
    first.move(10)
    assert (second.start, second.stop, second.length) == (1, 3, 2)
