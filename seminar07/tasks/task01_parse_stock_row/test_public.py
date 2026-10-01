import pytest

from seminar07.tasks.task01_parse_stock_row.parse_stock_row import parse_stock_row


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("карандаш;12", ("карандаш", 12)),
        ("  цветной карандаш ; 002 ", ("цветной карандаш", 2)),
        ("ручка;+3", ("ручка", 3)),
        ("скрепка;1_0", ("скрепка", 10)),
        ("ручка;0", None),
        ("ручка;-2", None),
        ("ручка;три", None),
        ("ручка;3.5", None),
        ("ручка;", None),
        (";4", None),
        ("   ; 4 ", None),
        ("ручка", None),
        ("ручка;2;склад", None),
        ("ручка, синяя;2", None),
        ("ручка,2", None),
    ],
)
def test_parse_stock_row(raw: str, expected: tuple[str, int] | None) -> None:
    assert parse_stock_row(raw) == expected


def test_parsing_does_not_print(capsys: pytest.CaptureFixture[str]) -> None:
    parse_stock_row("ручка;2")
    parse_stock_row("ручка;не число")

    assert capsys.readouterr() == ("", "")
