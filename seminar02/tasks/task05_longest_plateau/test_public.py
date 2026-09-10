from seminar02.tasks.task05_longest_plateau.longest_plateau import longest_plateau


def test_finds_longest_plateau() -> None:
    assert longest_plateau([1, 1, 2, 2, 2, 1]) == (2, 3)


def test_equal_lengths_choose_first_plateau() -> None:
    assert longest_plateau([7, 7, 1, 1]) == (0, 2)


def test_single_value_is_plateau_of_length_one() -> None:
    assert longest_plateau([5]) == (0, 1)


def test_all_different_values_choose_first() -> None:
    assert longest_plateau([3, 1, 4]) == (0, 1)


def test_empty_input_has_no_plateau() -> None:
    assert longest_plateau([]) == (-1, 0)
