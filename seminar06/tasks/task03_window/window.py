class Window:
    def __init__(self, start: int, stop: int) -> None:
        raise NotImplementedError("Implement me")

    def get_start(self) -> int:
        raise NotImplementedError("Implement me")

    def set_start(self, value: int) -> None:
        raise NotImplementedError("Implement me")

    def get_stop(self) -> int:
        raise NotImplementedError("Implement me")

    def set_stop(self, value: int) -> None:
        raise NotImplementedError("Implement me")

    def get_length(self) -> int:
        raise NotImplementedError("Implement me")

    def move(self, delta: int) -> None:
        raise NotImplementedError("Implement me")

    start = property(get_start, set_start)
    stop = property(get_stop, set_stop)
    length = property(get_length)
