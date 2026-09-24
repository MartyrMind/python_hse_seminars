from typing import Any

from seminar05.tasks.task06_bind_call.bind_call import bind_call


def test_mixed_call_collects_variadics_and_positional_only_name_in_keywords() -> None:
    parameters = [("x", "p"), ("y", "n"), ("rest", "a"), ("flag", "k"), ("extra", "v")]
    result = bind_call(parameters, {"y": 2, "flag": False}, (1, 3, 4, 5), {"x": 99, "mode": "fast"})
    assert result == {
        "x": 1,
        "y": 3,
        "rest": (4, 5),
        "flag": False,
        "extra": {"x": 99, "mode": "fast"},
    }
    assert list(result) == ["x", "y", "rest", "flag", "extra"]


def test_named_arguments_and_defaults_fill_remaining_parameters() -> None:
    parameters = [("x", "p"), ("y", "n"), ("rest", "a"), ("flag", "k"), ("extra", "v")]
    assert bind_call(parameters, {"y": 2, "flag": False}, (1,), {"y": 7, "flag": True}) == {
        "x": 1,
        "y": 7,
        "rest": (),
        "flag": True,
        "extra": {},
    }
    assert bind_call(parameters, {"y": 2, "flag": False}, (1,), {}) == {
        "x": 1,
        "y": 2,
        "rest": (),
        "flag": False,
        "extra": {},
    }


def test_positional_only_default_does_not_consume_same_named_keyword() -> None:
    assert bind_call([("x", "p"), ("extra", "v")], {"x": 10}, (), {"x": 20}) == {
        "x": 10,
        "extra": {"x": 20},
    }


def test_variadic_parameter_names_can_also_be_payload_keywords() -> None:
    assert bind_call(
        [("args", "a"), ("kwargs", "v")], {}, (1,), {"args": "named", "kwargs": "also named"}
    ) == {
        "args": (1,),
        "kwargs": {"args": "named", "kwargs": "also named"},
    }


def test_keyword_only_parameter_does_not_take_positional_argument() -> None:
    assert bind_call([("values", "a"), ("limit", "k")], {"limit": 8}, (1, 2), {}) == {
        "values": (1, 2),
        "limit": 8,
    }


def test_no_variadic_parameters_and_empty_signature() -> None:
    assert bind_call([("x", "n"), ("flag", "k")], {"flag": False}, (), {"x": 0}) == {
        "x": 0,
        "flag": False,
    }
    assert bind_call([], {}, (), {}) == {}


def test_all_positional_and_all_keyword_only_parameters() -> None:
    assert bind_call([("a", "p"), ("b", "p")], {"b": 9}, (1,), {}) == {"a": 1, "b": 9}
    assert bind_call([("a", "k"), ("b", "k")], {"b": None}, (), {"a": False}) == {
        "a": False,
        "b": None,
    }


def test_inputs_are_unchanged_and_bound_values_keep_identity() -> None:
    supplied: list[int] = []
    default: list[int] = []
    parameters = [("x", "n"), ("y", "k"), ("extra", "v")]
    original_parameters = parameters.copy()
    defaults: dict[str, Any] = {"y": default}
    kwargs: dict[str, Any] = {"x": supplied, "other": supplied}
    result = bind_call(parameters, defaults, (), kwargs)
    assert parameters == original_parameters
    assert kwargs == {"x": [], "other": []}
    assert defaults == {"y": []}
    assert result["x"] is supplied
    assert result["y"] is default
    assert result["extra"]["other"] is supplied
    result["extra"].clear()
    assert kwargs == {"x": [], "other": []}


def test_default_objects_are_reused_but_result_mappings_are_independent() -> None:
    default: list[int] = []
    parameters = [("x", "n"), ("extra", "v")]
    first = bind_call(parameters, {"x": default}, (), {})
    second = bind_call(parameters, {"x": default}, (), {})
    assert first is not second
    assert first["x"] is second["x"] is default
    assert first["extra"] is not second["extra"]
    first["extra"]["new"] = 1
    assert second["extra"] == {}


def test_remaining_keywords_keep_their_original_order() -> None:
    result = bind_call([("x", "n"), ("extra", "v")], {}, (), {"z": 1, "x": 2, "a": 3})
    assert result == {"x": 2, "extra": {"z": 1, "a": 3}}
    assert list(result["extra"]) == ["z", "a"]


def test_positional_values_keep_identity_in_regular_and_variadic_parameters() -> None:
    shared: list[int] = []
    args = (shared, shared)
    result = bind_call([("first", "n"), ("rest", "a")], {}, args, {})
    assert result["first"] is shared
    assert result["rest"][0] is shared
    assert args == ([], [])
