Config = dict[str, object]


def changes(before: Config, after: Config) -> dict[str, str]:
    raise NotImplementedError("Implement me")
