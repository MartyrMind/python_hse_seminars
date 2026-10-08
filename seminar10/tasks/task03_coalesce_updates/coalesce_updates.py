from collections import OrderedDict
from collections.abc import Iterable


def coalesce_updates[T](updates: Iterable[tuple[str, T]]) -> OrderedDict[str, T]:
    raise NotImplementedError("Implement me")
