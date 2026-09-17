from seminar03.tasks.task02_compare_attendance.compare_attendance import compare_attendance


def test_splits_students_into_three_groups() -> None:
    assert compare_attendance(
        ["Аня", "Борис", "Вера"],
        ["Борис", "Вера", "Глеб"],
    ) == (["Борис", "Вера"], ["Аня"], ["Глеб"])


def test_sorts_every_group_alphabetically() -> None:
    assert compare_attendance(
        ["Яна", "Борис", "Анна"],
        ["Юля", "Анна", "Вера"],
    ) == (["Анна"], ["Борис", "Яна"], ["Вера", "Юля"])


def test_repetitions_do_not_duplicate_students() -> None:
    assert compare_attendance(["Аня", "Аня", "Борис"], ["Аня", "Аня"]) == (
        ["Аня"],
        ["Борис"],
        [],
    )


def test_names_are_case_sensitive() -> None:
    assert compare_attendance(["Анна"], ["анна"]) == ([], ["Анна"], ["анна"])


def test_empty_lists_are_supported() -> None:
    assert compare_attendance([], []) == ([], [], [])
    assert compare_attendance(["Аня"], []) == ([], ["Аня"], [])
    assert compare_attendance([], ["Аня"]) == ([], [], ["Аня"])


def test_does_not_change_inputs() -> None:
    planned = ["Аня", "Борис"]
    actual = ["Борис", "Вера"]
    compare_attendance(planned, actual)
    assert planned == ["Аня", "Борис"]
    assert actual == ["Борис", "Вера"]
