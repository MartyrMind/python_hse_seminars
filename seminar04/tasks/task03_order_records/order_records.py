from typing import TypedDict


class Record(TypedDict):
    group: str
    score: int
    name: str


def ordered_records(records: list[Record]) -> list[Record]:
    raise NotImplementedError("Implement me")


def order_records_in_place(records: list[Record]) -> None:
    raise NotImplementedError("Implement me")
