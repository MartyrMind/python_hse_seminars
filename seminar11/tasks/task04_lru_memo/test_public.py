import inspect
from collections.abc import Callable
from typing import Any

import pytest

from seminar11.tasks.task04_lru_memo.lru_memo import LRUMemo

pytestmark = pytest.mark.timeout(5)


def test_equivalent_calls_and_defaults_share_one_entry() -> None:
    calls: list[tuple[int, int]] = []

    @LRUMemo(3)
    def calculate(a: int, b: int = 2) -> object:
        calls.append((a, b))
        return object()

    assert calls == []
    assert (calculate.hits, calculate.misses, calculate.cache_size()) == (0, 0, 0)
    first = calculate(1)
    assert calculate(a=1) is first
    assert calculate(1, 2) is first
    assert calculate(b=2, a=1) is first
    assert calls == [(1, 2)]
    assert (calculate.hits, calculate.misses, calculate.cache_size()) == (3, 1, 1)


def test_positional_only_keyword_only_and_variadic_parameters() -> None:
    calls = 0

    @LRUMemo(5)
    def calculate(a: int = 1, /, *values: int, scale: int = 2, **options: int) -> object:
        nonlocal calls
        calls += 1
        return object()

    empty = calculate()
    assert calculate(1, scale=2) is empty
    full = calculate(1, 2, 3, scale=4, bias=5, tax=6)
    assert calculate(1, 2, 3, tax=6, bias=5, scale=4) is full
    changed = calculate(1, 2, 3, scale=5, tax=6, bias=5)
    assert changed is not full
    assert calls == 3
    assert (calculate.hits, calculate.misses) == (2, 3)


def test_positional_parameter_and_same_name_in_extra_keywords_stay_distinct() -> None:
    @LRUMemo(3)
    def calculate(value: int, /, **options: int) -> object:
        return object()

    first = calculate(1, value=2)
    assert calculate(1, value=2) is first
    assert calculate(2, value=1) is not first
    assert (calculate.hits, calculate.misses) == (1, 2)


def test_hit_promotes_entry_so_eviction_is_lru_instead_of_fifo() -> None:
    calls: list[int] = []

    @LRUMemo(2)
    def calculate(value: int) -> object:
        calls.append(value)
        return object()

    first = calculate(1)
    second = calculate(2)
    assert calculate(1) is first
    calculate(3)  # вытесняется 2, потому что к 1 только что обращались
    assert calculate(1) is first
    assert calculate(2) is not second
    assert calls == [1, 2, 3, 2]
    assert calculate.cache_size() == 2
    assert (calculate.hits, calculate.misses) == (2, 4)


def test_capacity_one_keeps_only_the_most_recent_key() -> None:
    calls: list[int] = []

    @LRUMemo(1)
    def calculate(value: int) -> int:
        calls.append(value)
        return value * 10

    assert [calculate(1), calculate(1), calculate(2), calculate(1)] == [10, 10, 20, 10]
    assert calls == [1, 2, 1]
    assert calculate.cache_size() == 1


@pytest.mark.parametrize("result", [None, False, 0, "", [], {}])
def test_false_results_and_mutable_results_are_cached_by_identity(result: object) -> None:
    calls = 0

    @LRUMemo(2)
    def calculate() -> object:
        nonlocal calls
        calls += 1
        return result

    assert calculate() is result
    assert calculate() is result
    assert calls == 1
    assert (calculate.hits, calculate.misses) == (1, 1)


def test_failures_are_misses_but_do_not_cache_or_evict_existing_results() -> None:
    calls: list[int] = []
    error = ValueError("временно не получилось")

    @LRUMemo(1)
    def calculate(value: int) -> object:
        calls.append(value)
        if value == 2:
            raise error
        return object()

    first = calculate(1)
    for _ in range(2):
        with pytest.raises(ValueError) as caught:
            calculate(2)
        assert caught.value is error
        assert calculate.cache_size() == 1
    assert calculate(1) is first
    assert calls == [1, 2, 2]
    assert (calculate.hits, calculate.misses) == (1, 3)


def test_clear_resets_cache_and_counters_without_changing_original_function() -> None:
    calls = 0

    @LRUMemo(2)
    def calculate() -> object:
        nonlocal calls
        calls += 1
        return object()

    first = calculate()
    assert calculate() is first
    calculate.cache_clear()
    assert (calculate.hits, calculate.misses, calculate.cache_size()) == (0, 0, 0)
    assert calculate() is not first
    assert calls == 2
    assert (calculate.hits, calculate.misses) == (0, 1)


def test_reusing_one_decorator_object_does_not_share_caches_or_statistics() -> None:
    decorate = LRUMemo(2)

    @decorate
    def first(value: int) -> tuple[str, int]:
        return "first", value

    @decorate
    def second(value: int) -> tuple[str, int]:
        return "second", value

    assert first(1) == ("first", 1)
    assert first(1) == ("first", 1)
    assert second(1) == ("second", 1)
    assert (first.hits, first.misses, second.hits, second.misses) == (1, 1, 0, 1)
    first.cache_clear()
    assert second(1) == ("second", 1)
    assert (second.hits, second.misses, second.cache_size()) == (1, 1, 1)


def test_equal_hashes_do_not_make_different_arguments_the_same_key() -> None:
    class Token:
        def __init__(self, name: str) -> None:
            self.name = name

        def __hash__(self) -> int:
            return 0

        def __eq__(self, other: object) -> bool:
            return isinstance(other, Token) and self.name == other.name

    @LRUMemo(3)
    def calculate(token: Token) -> object:
        return object()

    first = calculate(Token("a"))
    second = calculate(Token("b"))
    assert first is not second
    assert calculate(Token("a")) is first
    assert calculate(Token("b")) is second
    assert (calculate.hits, calculate.misses) == (2, 2)


def test_unhashable_arguments_do_not_call_function_or_change_statistics() -> None:
    calls = 0

    @LRUMemo(2)
    def calculate(value: object, **options: object) -> object:
        nonlocal calls
        calls += 1
        return object()

    first = calculate(1)
    with pytest.raises(TypeError):
        calculate([])
    with pytest.raises(TypeError):
        calculate(value={})
    with pytest.raises(TypeError):
        calculate(1, extra=[])
    assert calls == 1
    assert (calculate.hits, calculate.misses, calculate.cache_size()) == (0, 1, 1)
    assert calculate(1) is first


def test_default_argument_is_also_part_of_hashability_check() -> None:
    default: list[int] = []
    calls = 0

    @LRUMemo(2)
    def calculate(value: list[int] = default) -> int:
        nonlocal calls
        calls += 1
        return len(value)

    with pytest.raises(TypeError):
        calculate()
    assert calls == 0
    assert (calculate.hits, calculate.misses, calculate.cache_size()) == (0, 0, 0)


def test_invalid_call_does_not_count_as_a_miss() -> None:
    calls = 0

    @LRUMemo(2)
    def calculate(value: int, /, *, scale: int) -> int:
        nonlocal calls
        calls += 1
        return value * scale

    dynamic: Any = calculate
    for args, kwargs in [
        ((1,), {}),
        ((), {"value": 1, "scale": 2}),
        ((1,), {"scale": 2, "unknown": 3}),
        ((1, 2), {"scale": 2}),
    ]:
        with pytest.raises(TypeError):
            dynamic(*args, **kwargs)
    assert calls == 0
    assert (calculate.hits, calculate.misses, calculate.cache_size()) == (0, 0, 0)


def test_metadata_and_signature_are_preserved() -> None:
    def calculate(value: int, *, scale: int = 2) -> int:
        """Расчёт цены."""
        return value * scale

    cached = LRUMemo(2)(calculate)
    metadata: Any = cached
    assert metadata.__name__ == "calculate"
    assert cached.__doc__ == "Расчёт цены."
    assert inspect.unwrap(cached) is calculate
    assert inspect.signature(cached) == inspect.signature(calculate)
    assert calculate(3) == 6
    assert (cached.hits, cached.misses) == (0, 0)


@pytest.mark.parametrize("capacity", [0, -1, -100])
def test_capacity_is_checked_when_creating_decorator(capacity: int) -> None:
    with pytest.raises(ValueError):
        LRUMemo(capacity)


@pytest.mark.parametrize("layers", [1, 2])
def test_wraps_preserves_full_metadata_at_each_layer(
    layers: int, assert_metadata: Callable[[Any, Any], None]
) -> None:
    def calculate[T](value: T, /, *, currency: str = "RUB") -> T:
        """Рассчитать цену."""
        return value

    calculate.__dict__["audit_tag"] = object()
    wrapped: Any = calculate
    for _ in range(layers):
        original = wrapped
        wrapped = LRUMemo(2)(original)
        assert_metadata(wrapped, original)

    assert wrapped(10, currency="EUR") == 10
    assert wrapped(10, currency="EUR") == 10
    assert (wrapped.hits, wrapped.misses) == (1, 1)
