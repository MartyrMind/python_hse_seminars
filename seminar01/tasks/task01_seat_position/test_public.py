from seminar01.tasks.task01_seat_position.seat_position import seat_position


def test_first_seat_is_at_left_edge() -> None:
    assert seat_position(1, 8) == (1, 1, True)


def test_last_seat_in_row_is_at_right_edge() -> None:
    assert seat_position(8, 8) == (1, 8, True)


def test_first_seat_in_later_row() -> None:
    assert seat_position(17, 8) == (3, 1, True)


def test_middle_seat_is_not_at_edge() -> None:
    assert seat_position(20, 8) == (3, 4, False)


def test_single_seat_row_is_always_at_edge() -> None:
    assert seat_position(7, 1) == (7, 1, True)
