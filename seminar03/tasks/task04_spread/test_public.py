from seminar03.tasks.task04_spread.spread import Cell, spread

EMPTY: set[Cell] = set()


def test_drop_in_middle_becomes_cross() -> None:
    assert spread({(1, 1)}, EMPTY, 3) == {(1, 1), (0, 1), (2, 1), (1, 0), (1, 2)}


def test_corner_has_only_two_new_neighbours() -> None:
    assert spread({(0, 0)}, EMPTY, 3) == {(0, 0), (0, 1), (1, 0)}


def test_walls_and_field_border_stop_water() -> None:
    assert spread({(0, 1)}, {(1, 1)}, 3) == {(0, 0), (0, 1), (0, 2)}


def test_diagonal_cells_are_not_neighbours() -> None:
    result = spread({(1, 1)}, EMPTY, 3)
    assert (0, 0) not in result
    assert (2, 2) not in result


def test_two_drops_grow_together_without_duplicates() -> None:
    assert spread({(0, 0), (0, 2)}, EMPTY, 3) == {
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 0),
        (1, 2),
    }


def test_empty_water_stays_empty() -> None:
    assert spread(EMPTY, EMPTY, 4) == set()


def test_full_field_stays_full() -> None:
    water = {(row, col) for row in range(2) for col in range(2)}
    result = spread(water, EMPTY, 2)
    assert result == water
    assert result is not water


def test_arguments_are_unchanged_and_result_is_new() -> None:
    water = {(1, 1)}
    walls = {(0, 1)}
    result = spread(water, walls, 3)
    assert water == {(1, 1)}
    assert walls == {(0, 1)}
    assert result is not water
