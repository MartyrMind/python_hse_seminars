from seminar03.tasks.task05_typed_counts.typed_counts import Scalar, typed_counts


def assert_typed_result(
    actual: list[tuple[Scalar, int]], expected: list[tuple[type[object], Scalar, int]]
) -> None:
    assert len(actual) == len(expected)
    for (actual_value, actual_count), (expected_type, expected_value, expected_count) in zip(
        actual, expected, strict=True
    ):
        assert type(actual_value) is expected_type
        assert actual_value == expected_value
        assert actual_count == expected_count


def test_counts_ordinary_repeated_values() -> None:
    assert typed_counts(["new", "done", "new"]) == [("new", 2), ("done", 1)]


def test_distinguishes_equal_numeric_values_of_different_types() -> None:
    actual = typed_counts([1, True, 1.0, 1, True])
    assert_typed_result(actual, [(int, 1, 2), (bool, True, 2), (float, 1.0, 1)])


def test_distinguishes_zero_false_and_float_zero() -> None:
    actual = typed_counts([0, False, 0.0])
    assert_typed_result(actual, [(int, 0, 1), (bool, False, 1), (float, 0.0, 1)])


def test_distinguishes_text_from_number() -> None:
    actual = typed_counts(["1", 1, "1"])
    assert_typed_result(actual, [(str, "1", 2), (int, 1, 1)])


def test_counts_none_as_an_ordinary_value() -> None:
    actual = typed_counts([None, 0, None])
    assert_typed_result(actual, [(type(None), None, 2), (int, 0, 1)])


def test_empty_input_produces_empty_list() -> None:
    assert typed_counts([]) == []


def test_does_not_change_input() -> None:
    values: list[Scalar] = [1, True, "1"]
    typed_counts(values)
    assert len(values) == 3
    assert type(values[0]) is int
    assert type(values[1]) is bool
    assert type(values[2]) is str
