from pathlib import Path

from seminar02.tasks.task07_cashflow_stats.cashflow_stats import cashflow_stats


def test_sums_income_expenses_and_balance(tmp_path: Path) -> None:
    path = tmp_path / "cashflow.txt"
    path.write_text("+ 1000\n- 250\n+ 75\n", encoding="utf-8")
    assert cashflow_stats(str(path)) == (3, 1075, 250, 825)


def test_ignores_blank_lines_and_comments(tmp_path: Path) -> None:
    path = tmp_path / "cashflow.txt"
    path.write_text("\n  # opening balance\n + 40\n   \n- 15\n", encoding="utf-8")
    assert cashflow_stats(str(path)) == (2, 40, 15, 25)


def test_stop_ignores_remaining_file(tmp_path: Path) -> None:
    path = tmp_path / "cashflow.txt"
    path.write_text("+ 10\nSTOP\n+ 1000\n", encoding="utf-8")
    assert cashflow_stats(str(path)) == (1, 10, 0, 10)


def test_empty_file_has_zero_statistics(tmp_path: Path) -> None:
    path = tmp_path / "cashflow.txt"
    path.write_text("", encoding="utf-8")
    assert cashflow_stats(str(path)) == (0, 0, 0, 0)
