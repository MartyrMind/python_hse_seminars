from seminar02.tasks.task09_bonus_shift_digits.shift_digits import shift_digits


def test_shifts_ascii_digits_cyclically() -> None:
    assert shift_digits("Meet at 19:58", 3) == "Meet at 42:81"


def test_negative_shift_wraps_backwards() -> None:
    assert shift_digits("Room 0", -1) == "Room 9"


def test_full_circle_changes_nothing() -> None:
    assert shift_digits("Code 907", 10) == "Code 907"


def test_non_ascii_digits_and_other_characters_stay_unchanged() -> None:
    assert shift_digits("²٣ and 5", 1) == "²٣ and 6"
