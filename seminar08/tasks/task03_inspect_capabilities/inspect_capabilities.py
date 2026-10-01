from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class CapabilityReport:
    has_getitem: bool
    iterable_abc: bool
    iter_starts: bool
    hashable_abc: bool
    hash_works: bool


def inspect_capabilities(value: Any) -> CapabilityReport:
    raise NotImplementedError("Implement me")
