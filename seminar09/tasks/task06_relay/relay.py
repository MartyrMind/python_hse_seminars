from collections.abc import Generator


def relay[Y, S, R](worker: Generator[Y, S, R], events: list[str]) -> Generator[Y, S, R]:
    raise NotImplementedError("Implement me")
