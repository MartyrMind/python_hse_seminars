import inspect
import warnings

import pytest

from seminar07.tasks.task04_normalize_rows.normalize_rows import StockRow, normalize_rows


def test_version_one_rows_are_normalized_in_order() -> None:
    rows = [StockRow("ручка", 2, 1), StockRow("карандаш", 3, 2), StockRow("ластик", 1, 1)]

    normalized, recorded = normalize_rows(rows)

    assert normalized == [
        StockRow("ручка", 2, 2),
        StockRow("карандаш", 3, 2),
        StockRow("ластик", 1, 2),
    ]
    assert len(recorded) == 2
    assert [warning.category for warning in recorded] == [DeprecationWarning] * 2
    assert "1" in str(recorded[0].message)
    assert "3" in str(recorded[1].message)
    assert rows == [StockRow("ручка", 2, 1), StockRow("карандаш", 3, 2), StockRow("ластик", 1, 1)]
    assert normalized is not rows


def test_version_two_and_empty_input_have_no_warnings() -> None:
    assert normalize_rows([]) == ([], [])
    assert normalize_rows([StockRow("ручка", 2, 2)]) == ([StockRow("ручка", 2, 2)], [])
    assert normalize_rows([StockRow("ручка", 2, 2)], strict=True) == (
        [StockRow("ручка", 2, 2)],
        [],
    )


def test_every_legacy_row_is_reported_even_under_external_ignore_filter() -> None:
    rows = [StockRow("ручка", 2, 1), StockRow("ручка", 2, 1)]

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        normalized, recorded = normalize_rows(rows)

    assert normalized == [StockRow("ручка", 2, 2), StockRow("ручка", 2, 2)]
    assert len(recorded) == 2
    assert [str(warning.message) for warning in recorded] != ["", ""]


def test_strict_mode_raises_first_deprecation_warning() -> None:
    rows = [StockRow("новый", 5, 2), StockRow("старый", 2, 1), StockRow("ещё", 3, 1)]

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        with pytest.raises(DeprecationWarning) as caught:
            normalize_rows(rows, strict=True)

    assert "2" in str(caught.value)
    assert rows[1].version == 1


def test_warning_filters_are_restored_after_success_and_failure() -> None:
    rows = [StockRow("ручка", 2, 1)]

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        before = list(warnings.filters)
        normalize_rows(rows)
        assert warnings.filters == before
        with pytest.raises(DeprecationWarning):
            normalize_rows(rows, strict=True)
        assert warnings.filters == before


def test_recorded_warning_points_to_call_site() -> None:
    line = inspect.currentframe().f_lineno + 1  # type: ignore[union-attr]
    _, recorded = normalize_rows([StockRow("ручка", 2, 1)])

    assert len(recorded) == 1
    assert recorded[0].filename == __file__
    assert recorded[0].lineno == line


def test_repeated_calls_do_not_leak_warning_state() -> None:
    rows = [StockRow("ручка", 2, 1)]
    first, first_warnings = normalize_rows(rows)
    second, second_warnings = normalize_rows(rows)

    assert first == second == [StockRow("ручка", 2, 2)]
    assert len(first_warnings) == len(second_warnings) == 1
