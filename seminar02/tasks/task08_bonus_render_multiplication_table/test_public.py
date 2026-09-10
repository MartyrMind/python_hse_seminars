from seminar02.tasks.task08_bonus_render_multiplication_table.render_multiplication_table import (
    render_multiplication_table,
)


def test_zero_size_produces_empty_table() -> None:
    assert render_multiplication_table(0) == []


def test_single_cell_table() -> None:
    assert render_multiplication_table(1) == ["1"]


def test_one_digit_cells_need_no_padding() -> None:
    assert render_multiplication_table(3) == ["1 2 3", "2 4 6", "3 6 9"]


def test_cells_align_to_largest_product() -> None:
    assert render_multiplication_table(4) == [
        " 1  2  3  4",
        " 2  4  6  8",
        " 3  6  9 12",
        " 4  8 12 16",
    ]
