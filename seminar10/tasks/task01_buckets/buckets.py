class Buckets[T]:
    def __init__(self) -> None:
        raise NotImplementedError("Implement me")

    def add(self, key: str, value: T) -> None:
        raise NotImplementedError("Implement me")

    def peek(self, key: str) -> list[T]:
        raise NotImplementedError("Implement me")

    def keys(self) -> list[str]:
        raise NotImplementedError("Implement me")
