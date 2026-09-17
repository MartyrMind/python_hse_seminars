import pytest

from seminar03.tasks.task01_count_statuses.count_statuses import count_statuses


@pytest.mark.timeout(3)
def test_many_distinct_statuses_finish_in_time() -> None:
    statuses = [f"status-{index:05d}" for index in range(60_000)]

    result = count_statuses(statuses)

    assert len(result) == 60_000
    assert result["status-00000"] == 1
    assert result["status-59999"] == 1
