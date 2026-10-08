class PriorityQueue[T]:
    def __init__(self) -> None:
        raise NotImplementedError("Implement me")

    def push(self, priority: int, item: T) -> None:
        raise NotImplementedError("Implement me")

    def peek(self) -> T:
        raise NotImplementedError("Implement me")

    def pop(self) -> T:
        raise NotImplementedError("Implement me")

    def __len__(self) -> int:
        raise NotImplementedError("Implement me")
