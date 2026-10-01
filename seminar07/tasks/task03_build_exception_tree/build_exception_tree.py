from __future__ import annotations

import traceback
from dataclasses import dataclass


@dataclass
class ErrorNode:
    error: BaseException
    frames: list[traceback.FrameSummary]
    children: list[tuple[str, ErrorNode]]


def build_exception_tree(errors: list[Exception]) -> ErrorNode:
    raise NotImplementedError("Implement me")
