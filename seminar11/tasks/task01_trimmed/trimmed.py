from collections.abc import Callable


def trimmed[**P](func: Callable[P, str]) -> Callable[P, str]:
    raise NotImplementedError("Implement me")
