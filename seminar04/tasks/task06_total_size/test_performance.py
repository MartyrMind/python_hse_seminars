import pytest

from seminar04.tasks.task06_total_size.total_size import Data, total_size


@pytest.mark.timeout(3)
def test_wide_structure_finishes_in_time() -> None:
    rows: list[list[Data]] = [[1_000_000 + index] for index in range(40_000)]
    data: list[Data] = list(rows)
    expected = data.__sizeof__() + sum(row.__sizeof__() + row[0].__sizeof__() for row in rows)

    assert total_size(data) == expected
