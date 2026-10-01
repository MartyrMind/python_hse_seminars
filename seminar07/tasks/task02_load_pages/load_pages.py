from collections.abc import Callable
from dataclasses import dataclass


@dataclass
class Page:
    rows: list[str]
    next_cursor: str | None


type Fetcher = Callable[[str | None], Page]


class PageLoadError(Exception):
    source: str
    page_number: int
    cursor: str | None

    def __init__(self, source: str, page_number: int, cursor: str | None) -> None:
        raise NotImplementedError("Implement me")


def load_pages(
    n: int,
    start_cursor: str | None,
    primary: Fetcher,
    reserve: Fetcher,
    save_all: Callable[[list[str]], None],
) -> list[str]:
    raise NotImplementedError("Implement me")
