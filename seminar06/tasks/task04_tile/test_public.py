import pytest

from seminar06.tasks.task04_tile.tile import Tile


@pytest.mark.parametrize(
    "colors",
    [("a", "b", "c", "d"), ("b", "c", "d", "a"), ("c", "d", "a", "b"), ("d", "a", "b", "c")],
)
def test_all_rotations_are_equal_and_interchangeable_as_keys(
    colors: tuple[str, str, str, str],
) -> None:
    first = Tile(("a", "b", "c", "d"))
    rotated = Tile(colors)
    assert first is not rotated
    assert first == rotated
    assert rotated == first
    assert hash(first) == hash(rotated)
    assert len({first, rotated}) == 1
    assert {first: "found"}[rotated] == "found"


@pytest.mark.parametrize("colors", [("a", "d", "c", "b"), ("a", "c", "b", "d")])
def test_same_colors_in_a_different_circular_order_are_not_equal(
    colors: tuple[str, str, str, str],
) -> None:
    first = Tile(("a", "b", "c", "d"))
    other = Tile(colors)
    assert first != other
    assert len({first, other}) == 2


def test_repeated_colors_can_have_fewer_than_four_distinct_rotations() -> None:
    striped = Tile(("a", "b", "a", "b"))
    rotated = Tile(("b", "a", "b", "a"))
    adjacent = Tile(("a", "a", "b", "b"))
    assert striped == rotated
    assert striped != adjacent
    assert len({striped, rotated, adjacent}) == 2


def test_plain_tiles_and_empty_color_names() -> None:
    first = Tile(("", "", "", ""))
    second = Tile(("", "", "", ""))
    red = Tile(("red", "red", "red", "red"))
    assert first == second
    assert len({first, second, red}) == 2


def test_rotations_with_repeated_colors_and_different_neighbors() -> None:
    first = Tile(("a", "b", "a", "c"))
    rotated = Tile(("a", "c", "a", "b"))
    assert first == rotated
    assert hash(first) == hash(rotated)
    assert len({first, rotated}) == 1


def test_input_tuple_is_not_changed() -> None:
    colors = ("d", "a", "b", "c")
    tile = Tile(colors)
    assert tile == Tile(("a", "b", "c", "d"))
    assert colors == ("d", "a", "b", "c")
