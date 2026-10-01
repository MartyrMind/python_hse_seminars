import warnings
from dataclasses import dataclass


@dataclass(frozen=True)
class StockRow:
    product: str
    quantity: int
    version: int


def normalize_rows(
    rows: list[StockRow], *, strict: bool = False
) -> tuple[list[StockRow], list[warnings.WarningMessage]]:
    raise NotImplementedError("Implement me")
