Data = int | str | list["Data"] | dict[str, "Data"]


class FrozenKey:
    def __init__(self, data: Data) -> None:
        raise NotImplementedError("Implement me")
