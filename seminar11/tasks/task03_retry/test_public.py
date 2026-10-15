from collections.abc import Callable
from inspect import unwrap
from typing import Any

import pytest

from seminar11.tasks.task03_retry.retry import retry

pytestmark = pytest.mark.timeout(5)


@pytest.mark.parametrize("result", [None, False, 0, "", [], object()])
def test_first_success_is_returned_as_is_without_more_calls(result: object) -> None:
    calls = 0

    @retry(3, (TimeoutError,))
    def load() -> object:
        nonlocal calls
        calls += 1
        return result

    assert calls == 0
    assert load() is result
    assert calls == 1


def test_success_stops_retries_and_next_invocation_gets_a_fresh_budget() -> None:
    calls: list[int] = []

    @retry(attempts=3, errors=(TimeoutError,))
    def load() -> int:
        calls.append(len(calls) + 1)
        if len(calls) % 3 != 0:
            raise TimeoutError("временно")
        return len(calls)

    assert load() == 3
    assert calls == [1, 2, 3]
    assert load() == 6
    assert calls == [1, 2, 3, 4, 5, 6]


def test_last_original_exception_is_raised_and_attempts_include_first_call() -> None:
    errors = [TimeoutError("первая"), TimeoutError("вторая"), TimeoutError("последняя")]
    calls = 0

    @retry(3, (TimeoutError,))
    def fail() -> None:
        nonlocal calls
        error = errors[calls]
        calls += 1
        raise error

    with pytest.raises(TimeoutError) as caught:
        fail()
    assert caught.value is errors[2]
    assert calls == 3


def test_one_attempt_does_not_retry() -> None:
    calls = 0

    @retry(1, (ValueError,))
    def fail() -> None:
        nonlocal calls
        calls += 1
        raise ValueError("ошибка")

    with pytest.raises(ValueError):
        fail()
    assert calls == 1


def test_caught_subclasses_and_multiple_exception_types() -> None:
    calls = 0

    class Temporary(TimeoutError):
        pass

    @retry(4, (TimeoutError, ConnectionError))
    def load() -> str:
        nonlocal calls
        calls += 1
        if calls == 1:
            raise Temporary()
        if calls == 2:
            raise ConnectionError()
        return "готово"

    assert load() == "готово"
    assert calls == 3


def test_unlisted_error_stops_even_after_a_retry() -> None:
    calls = 0
    error = TypeError("повторять бесполезно")

    @retry(5, (TimeoutError,))
    def fail() -> None:
        nonlocal calls
        calls += 1
        if calls == 1:
            raise TimeoutError()
        raise error

    with pytest.raises(TypeError) as caught:
        fail()
    assert caught.value is error
    assert calls == 2


def test_base_exception_is_not_caught_by_exception_handler() -> None:
    class StopWork(BaseException):
        pass

    error = StopWork()
    calls = 0

    @retry(3, (Exception,))
    def stop() -> None:
        nonlocal calls
        calls += 1
        raise error

    with pytest.raises(StopWork) as caught:
        stop()
    assert caught.value is error
    assert calls == 1


def test_argument_objects_and_mutations_survive_between_attempts() -> None:
    rows: list[int] = []
    options: dict[str, int] = {}

    @retry(3, (TimeoutError,))
    def load(data: list[int], /, *, settings: dict[str, int]) -> list[int]:
        assert data is rows
        assert settings is options
        data.append(1)
        if len(data) < 2:
            raise TimeoutError()
        return data

    assert load(rows, settings=options) is rows
    assert rows == [1, 1]


@pytest.mark.parametrize("attempts", [0, -1, -3])
def test_attempt_count_is_checked_before_decoration(attempts: int) -> None:
    with pytest.raises(ValueError):
        retry(attempts, (ValueError,))


def test_empty_exception_tuple_is_checked_before_decoration() -> None:
    with pytest.raises(ValueError):
        retry(2, ())


def test_metadata_and_independence_when_reusing_factory() -> None:
    decorate = retry(2, (TimeoutError,))

    def first(value: int) -> int:
        """Первый источник."""
        return value

    wrapped = decorate(first)
    other = decorate(str)
    assert wrapped.__name__ == "first"
    assert wrapped.__doc__ == "Первый источник."
    assert unwrap(wrapped) is first
    assert wrapped(4) == 4
    assert other(5) == "5"
    assert wrapped(6) == 6


@pytest.mark.parametrize("layers", [1, 2])
def test_wraps_preserves_full_metadata_at_each_layer(
    layers: int, assert_metadata: Callable[[Any, Any], None]
) -> None:
    def load[T](value: T, /, *, source: str = "main") -> T:
        """Загрузить запись."""
        return value

    load.__dict__["audit_tag"] = object()
    wrapped = load
    for _ in range(layers):
        original = wrapped
        wrapped = retry(2, (TimeoutError,))(original)
        assert_metadata(wrapped, original)

    value = object()
    assert wrapped(value, source="backup") is value
