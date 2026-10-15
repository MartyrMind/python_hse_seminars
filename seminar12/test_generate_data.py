"""Проверки CLI генератора; задания студент выполняет в ноутбуке."""

import csv
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

import pytest

SCRIPT = Path(__file__).with_name("generate_data.py")


def generate(output: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--output-dir", str(output), *arguments],
        cwd=output.parent,
        capture_output=True,
        text=True,
        check=False,
    )


def test_csvs_describe_consecutive_days_and_matching_drinks(tmp_path: Path) -> None:
    output = tmp_path / "coffee"
    result = generate(output, "--seed", "42", "--days", "28")
    assert result.returncode == 0, result.stderr
    with (output / "sales.csv").open(encoding="utf-8", newline="") as stream:
        sales = list(csv.DictReader(stream))
    with (output / "prices.csv").open(encoding="utf-8", newline="") as stream:
        prices = list(csv.DictReader(stream))

    assert len(sales) == 28
    assert len(prices) == 4
    drinks = [row["drink"] for row in prices]
    assert list(sales[0]) == ["date", *drinks]
    assert all(float(row["price"]) > 0 for row in prices)
    first = date.fromisoformat(sales[0]["date"])
    assert [row["date"] for row in sales] == [
        (first + timedelta(days=offset)).isoformat() for offset in range(28)
    ]
    quantities = [int(row[drink]) for row in sales for drink in drinks]
    assert all(quantity >= 0 for quantity in quantities)
    assert len(set(quantities)) > 1


def test_seed_reproduces_the_csv_bytes(tmp_path: Path) -> None:
    first, second, different = [tmp_path / name for name in ("a", "b", "c")]
    for output, seed in [(first, "17"), (second, "17"), (different, "18")]:
        result = generate(output, "--seed", seed)
        assert result.returncode == 0, result.stderr
    for name in ("sales.csv", "prices.csv"):
        assert (first / name).read_bytes() == (second / name).read_bytes()
    assert (first / "sales.csv").read_bytes() != (different / "sales.csv").read_bytes()


def test_start_date_and_one_day(tmp_path: Path) -> None:
    output = tmp_path / "coffee"
    result = generate(output, "--days", "1", "--start-date", "2026-12-31")
    assert result.returncode == 0, result.stderr
    with (output / "sales.csv").open(encoding="utf-8", newline="") as stream:
        sales = list(csv.DictReader(stream))
    assert len(sales) == 1
    assert sales[0]["date"] == "2026-12-31"


@pytest.mark.parametrize(
    "arguments",
    [("--days", "0"), ("--days", "-1"), ("--start-date", "2026-02-30")],
)
def test_invalid_arguments_do_not_create_output(tmp_path: Path, arguments: tuple[str, ...]) -> None:
    output = tmp_path / "coffee"
    result = generate(output, *arguments)
    assert result.returncode == 2
    assert "error:" in result.stderr
    assert not output.exists()
