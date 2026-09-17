import pytest

from seminar03.tasks.task04_spread.spread import Cell, spread


@pytest.mark.timeout(3)
def test_large_full_field_finishes_in_time() -> None:
    size = 250
    water: set[Cell] = {(row, col) for row in range(size) for col in range(size)}

    result = spread(water, set(), size)

    assert result == water
    assert result is not water
