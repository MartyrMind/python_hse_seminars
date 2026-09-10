from seminar02.tasks.task02_digital_root_steps.digital_root_steps import digital_root_steps


def test_zero_needs_no_steps() -> None:
    assert digital_root_steps(0) == (0, 0)


def test_one_digit_needs_no_steps() -> None:
    assert digital_root_steps(7) == (7, 0)


def test_two_digit_number_needs_multiple_steps() -> None:
    assert digital_root_steps(38) == (2, 2)


def test_large_number() -> None:
    assert digital_root_steps(9875) == (2, 3)


def test_many_equal_digits() -> None:
    assert digital_root_steps(999_999) == (9, 2)
