Data = int | str | list["Data"] | dict[str, "Data"]


def total_size(data: Data) -> int:
    raise NotImplementedError("Implement me")
