import pytest

from seminar03.tasks.task05_typed_counts.typed_counts import Scalar, typed_counts


@pytest.mark.timeout(3)
def test_many_typed_groups_finish_in_time() -> None:
    values: list[Scalar] = list(range(60_000))

    result = typed_counts(values)

    assert len(result) == 60_000
    assert result[0] == (0, 1)
    assert result[-1] == (59_999, 1)
