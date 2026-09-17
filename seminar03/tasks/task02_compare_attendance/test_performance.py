import pytest

from seminar03.tasks.task02_compare_attendance.compare_attendance import compare_attendance


@pytest.mark.timeout(3)
def test_large_attendance_lists_finish_in_time() -> None:
    planned = [f"student-{index:05d}" for index in range(40_000)]
    actual = [f"student-{index:05d}" for index in range(20_000, 60_000)]

    present, absent, unexpected = compare_attendance(planned, actual)

    assert len(present) == len(absent) == len(unexpected) == 20_000
    assert (present[0], present[-1]) == ("student-20000", "student-39999")
    assert (absent[0], absent[-1]) == ("student-00000", "student-19999")
    assert (unexpected[0], unexpected[-1]) == ("student-40000", "student-59999")
