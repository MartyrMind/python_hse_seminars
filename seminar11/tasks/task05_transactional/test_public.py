from collections.abc import Callable
from inspect import unwrap
from typing import Any

import pytest

from seminar11.tasks.task05_transactional.transactional import Transactions

pytestmark = pytest.mark.timeout(5)


def test_success_commits_to_the_original_dictionary() -> None:
    state = {"mode": "normal"}
    alias = state
    tx = Transactions(state)
    with tx.atomic() as current:
        assert current is state
        current["mode"] = "debug"
        current["format"] = "json"
    assert alias is state
    assert list(alias.items()) == [("mode", "debug"), ("format", "json")]


def test_rollback_restores_values_keys_order_and_identity() -> None:
    state = {"first": 1, "second": 2, "third": 3}
    alias = state
    tx = Transactions(state)
    error = ValueError("откат")
    with pytest.raises(ValueError) as caught, tx.atomic():
        del state["first"]
        state["first"] = 10
        state["second"] = 20
        state["new"] = 4
        del state["third"]
        raise error
    assert caught.value is error
    assert alias is state
    assert list(alias.items()) == [("first", 1), ("second", 2), ("third", 3)]


def test_empty_snapshot_and_none_value_are_not_confused_with_missing_keys() -> None:
    state: dict[str, object] = {"exists": None}
    tx = Transactions(state)
    with pytest.raises(RuntimeError), tx.atomic():
        state.clear()
        state["new"] = None
        raise RuntimeError()
    assert state == {"exists": None}

    empty: dict[str, int] = {}
    with pytest.raises(RuntimeError), Transactions(empty).atomic():
        empty["new"] = 1
        raise RuntimeError()
    assert empty == {}


def test_snapshot_is_taken_on_entry_instead_of_manager_creation() -> None:
    state = {"value": 1}
    tx = Transactions(state)
    scope = tx.atomic()
    state["value"] = 2
    state["later"] = 3
    with pytest.raises(ValueError), scope:
        state.clear()
        raise ValueError()
    assert list(state.items()) == [("value", 2), ("later", 3)]


def test_shallow_rollback_restores_references_but_not_nested_mutations() -> None:
    values = [1]
    state: dict[str, object] = {"values": values}
    with pytest.raises(ValueError), Transactions(state).atomic():
        values.append(2)
        state["values"] = [99]
        raise ValueError()
    assert state["values"] is values
    assert values == [1, 2]


def test_inner_rollback_can_be_caught_and_outer_transaction_can_commit() -> None:
    state = {"value": 0}
    tx = Transactions(state)
    with tx.atomic():
        state["value"] = 1
        state["outer"] = 10
        with pytest.raises(ValueError), tx.atomic():
            state["value"] = 2
            state["inner"] = 20
            del state["outer"]
            raise ValueError()
        assert list(state.items()) == [("value", 1), ("outer", 10)]
        state["after"] = 30
    assert list(state.items()) == [("value", 1), ("outer", 10), ("after", 30)]


def test_outer_failure_also_rolls_back_successful_inner_transaction() -> None:
    state = {"value": 0}
    tx = Transactions(state)
    with pytest.raises(ValueError), tx.atomic():
        state["value"] = 1
        with tx.atomic():
            state["value"] = 2
            state["inner"] = 20
        assert state == {"value": 2, "inner": 20}
        raise ValueError()
    assert state == {"value": 0}


def test_propagating_inner_failure_rolls_back_all_open_scopes() -> None:
    state = {"value": 0}
    tx = Transactions(state)
    error = LookupError("глубокая ошибка")
    with pytest.raises(LookupError) as caught, tx.atomic():
        state["value"] = 1
        with tx.atomic():
            state["value"] = 2
            with tx.atomic():
                state["value"] = 3
                raise error
    assert caught.value is error
    assert state == {"value": 0}


def test_base_exception_also_rolls_back_and_is_not_suppressed() -> None:
    class Cancelled(BaseException):
        pass

    state = {"value": 0}
    error = Cancelled()
    with pytest.raises(Cancelled) as caught, Transactions(state).atomic():
        state["value"] = 1
        raise error
    assert caught.value is error
    assert state == {"value": 0}


def test_decorator_forwards_arguments_result_and_metadata_without_eager_work() -> None:
    state: dict[str, object] = {}
    tx = Transactions(state)
    result = object()
    values: list[int] = []

    def configure(data: list[int], /, *, mode: str) -> object:
        """Изменить настройки."""
        assert data is values
        state["mode"] = mode
        return result

    wrapped = tx.transactional(configure)
    assert state == {}
    assert wrapped.__name__ == "configure"
    assert wrapped.__doc__ == "Изменить настройки."
    assert unwrap(wrapped) is configure
    assert wrapped(values, mode="debug") is result
    assert state == {"mode": "debug"}


def test_decorated_calls_take_new_snapshots_and_work_after_failure() -> None:
    state = {"value": 0}
    tx = Transactions(state)
    error = ValueError("не приняли")

    @tx.transactional
    def configure(value: int, *, fail: bool = False) -> int:
        state["value"] = value
        if fail:
            raise error
        return value

    assert configure(1) == 1
    with pytest.raises(ValueError) as caught:
        configure(2, fail=True)
    assert caught.value is error
    assert state == {"value": 1}
    assert configure(3) == 3
    assert state == {"value": 3}


def test_context_and_decorator_share_nested_transaction_rules() -> None:
    state = {"value": 0}
    tx = Transactions(state)

    @tx.transactional
    def configure() -> None:
        state["value"] = 2
        with pytest.raises(ValueError), tx.atomic():
            state["value"] = 3
            raise ValueError()
        assert state["value"] == 2

    with pytest.raises(RuntimeError), tx.atomic():
        state["value"] = 1
        configure()
        assert state["value"] == 2
        raise RuntimeError()
    assert state == {"value": 0}


def test_recursive_decorated_function_has_a_snapshot_for_each_call() -> None:
    state: dict[str, Any] = {"depth": -1}
    tx = Transactions(state)

    @tx.transactional
    def descend(depth: int) -> None:
        state["depth"] = depth
        if depth == 0:
            state["temporary"] = True
            raise ValueError()
        if depth == 1:
            with pytest.raises(ValueError):
                descend(0)
            assert state["depth"] == 1
            assert "temporary" not in state
            state["recovered"] = True
        else:
            descend(depth - 1)

    descend(2)
    assert state == {"depth": 1, "recovered": True}
    with pytest.raises(RuntimeError), tx.atomic():
        descend(3)
        raise RuntimeError()
    assert state == {"depth": 1, "recovered": True}


def test_separate_managers_do_not_change_each_others_dictionaries() -> None:
    left = {"value": 1}
    right = {"value": 2}
    first, second = Transactions(left), Transactions(right)
    with pytest.raises(ValueError), first.atomic():
        left["value"] = 10
        with second.atomic():
            right["value"] = 20
        raise ValueError()
    assert left == {"value": 1}
    assert right == {"value": 20}
    with first.atomic():
        left["value"] = 30
    assert left == {"value": 30}


@pytest.mark.parametrize("layers", [1, 2])
def test_wraps_preserves_full_metadata_at_each_layer(
    layers: int, assert_metadata: Callable[[Any, Any], None]
) -> None:
    state: dict[str, object] = {}
    tx = Transactions(state)

    def configure[T](value: T, /, *, key: str = "value") -> T:
        """Изменить настройки."""
        state[key] = value
        return value

    configure.__dict__["audit_tag"] = object()
    wrapped = configure
    for _ in range(layers):
        original = wrapped
        wrapped = tx.transactional(original)
        assert_metadata(wrapped, original)

    value = object()
    assert wrapped(value, key="port") is value
    assert state["port"] is value
