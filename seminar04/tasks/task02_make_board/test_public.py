from seminar04.tasks.task02_make_board.make_board import make_board


def test_builds_board_with_requested_shape_and_fill() -> None:
    assert make_board(2, 3, 7) == [[7, 7, 7], [7, 7, 7]]


def test_rows_are_different_objects() -> None:
    board = make_board(3, 2)
    assert board[0] is not board[1]
    assert board[1] is not board[2]
    assert board[0] is not board[2]


def test_changing_one_cell_does_not_change_other_rows() -> None:
    board = make_board(3, 3)
    board[0][1] = 5
    assert board == [[0, 5, 0], [0, 0, 0], [0, 0, 0]]


def test_zero_rows_produces_empty_board() -> None:
    assert make_board(0, 4) == []


def test_zero_columns_produces_independent_empty_rows() -> None:
    board = make_board(2, 0)
    assert board == [[], []]
    assert board[0] is not board[1]


def test_single_row_and_column() -> None:
    assert make_board(1, 1, -3) == [[-3]]
