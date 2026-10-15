from collections.abc import Callable
from inspect import signature, unwrap
from typing import Any

import pytest


@pytest.fixture
def assert_metadata() -> Callable[[Any, Any], None]:
    def check(wrapped: Any, original: Any) -> None:
        assert wrapped is not original
        assert wrapped.__name__ == original.__name__
        assert wrapped.__qualname__ == original.__qualname__
        assert wrapped.__module__ == original.__module__
        assert wrapped.__doc__ == original.__doc__
        assert wrapped.__annotations__ == original.__annotations__
        if hasattr(original, "__annotate__"):
            assert wrapped.__annotate__ is original.__annotate__
        assert wrapped.__type_params__ == original.__type_params__
        assert wrapped.__dict__["audit_tag"] is original.__dict__["audit_tag"]
        assert wrapped.__wrapped__ is original
        assert unwrap(wrapped) is unwrap(original)
        assert signature(wrapped) == signature(original)

    return check
