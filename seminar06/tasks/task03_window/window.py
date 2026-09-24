class Window:
    start: int
    stop: int
    length: int

    def __init__(self, start: int, stop: int) -> None:
        raise NotImplementedError("Implement me")

    def move(self, delta: int) -> None:
        raise NotImplementedError("Implement me")
