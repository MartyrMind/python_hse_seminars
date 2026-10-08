from collections.abc import Iterator
from itertools import islice
from typing import cast

import pytest

from seminar10.tasks.task06_candidate_codes.candidate_codes import Mode, candidate_codes

pytestmark = pytest.mark.timeout(5)


@pytest.mark.parametrize(("mode", "expected"), [
    ("product", ["BB", "BA", "BC", "AB", "AA", "AC", "CB", "CA", "CC"]),
    ("permutations", ["BA", "BC", "AB", "AC", "CB", "CA"]),
    ("combinations", ["BA", "BC", "AC"]),
    ("replacement", ["BB", "BA", "BC", "AA", "AC", "CC"]),
])
def test_modes_preserve_input_order(mode: Mode, expected: list[str]) -> None:
    assert list(candidate_codes("BAC", 2, mode)) == expected


def test_limit_applies_after_filtering_and_forbidden_are_substrings() -> None:
    assert list(candidate_codes("AB", 3, "product", ("AA", "BB"), 2)) == ["ABA", "BAB"]
    assert list(candidate_codes("ABC", 2, "product", ("A",), 3)) == ["BB", "BC", "CB"]


@pytest.mark.parametrize("mode", ["product", "permutations", "combinations", "replacement"])
def test_duplicate_symbols_are_distinct_positions(mode: Mode) -> None:
    expected = {
        "product": ["AA", "AA", "AA", "AA"],
        "permutations": ["AA", "AA"],
        "combinations": ["AA"],
        "replacement": ["AA", "AA", "AA"],
    }
    assert list(candidate_codes("AA", 2, mode)) == expected[mode]


@pytest.mark.parametrize("mode", ["product", "permutations", "combinations", "replacement"])
def test_zero_length_has_one_empty_code(mode: Mode) -> None:
    assert list(candidate_codes("", 0, mode)) == [""]
    assert list(candidate_codes("AB", 0, mode, ("A",))) == [""]
    assert list(candidate_codes("AB", 0, mode, ("",))) == []


@pytest.mark.parametrize("mode", ["product", "permutations", "combinations", "replacement"])
def test_empty_alphabet_has_no_positive_length_codes(mode: Mode) -> None:
    assert list(candidate_codes("", 2, mode)) == []


@pytest.mark.parametrize("mode", ["permutations", "combinations"])
def test_impossible_choice_is_empty(mode: Mode) -> None:
    assert list(candidate_codes("AB", 3, mode)) == []


def test_entire_search_can_be_filtered_out() -> None:
    assert list(candidate_codes("AB", 2, "product", ("",))) == []
    assert list(candidate_codes("AB", 2, "product", ("A", "B"))) == []


def test_large_search_is_not_materialized() -> None:
    assert list(candidate_codes("AB", 30, "product", limit=2)) == ["A" * 30, "A" * 29 + "B"]
    assert list(islice(candidate_codes("AB", 30, "product", limit=1_000_000), 1)) == ["A" * 30]


def test_zero_limit_does_not_search() -> None:
    assert list(candidate_codes("AB", 30, "product", ("A", "B"), 0)) == []


def test_no_candidates_are_checked_after_the_answer_limit() -> None:
    checks: list[str] = []

    class Forbidden(tuple[str, ...]):
        def __iter__(self) -> Iterator[str]:
            checks.append("check")
            return super().__iter__()

    walk = candidate_codes("AB", 3, "product", Forbidden(("AA", "BB")), 1)
    assert checks == []
    assert next(walk) == "ABA"
    checks_after_answer = len(checks)
    with pytest.raises(StopIteration):
        next(walk)
    assert len(checks) == checks_after_answer


@pytest.mark.parametrize(("length", "limit"), [(-1, 1), (1, -1), (-1, 0)])
def test_negative_parameters_are_rejected_on_first_request(length: int, limit: int) -> None:
    walk = candidate_codes("AB", length, "product", limit=limit)
    with pytest.raises(ValueError):
        next(walk)


def test_unknown_mode_is_rejected_even_with_zero_limit() -> None:
    walk = candidate_codes("AB", 2, cast(Mode, "unknown"), limit=0)
    with pytest.raises(ValueError):
        next(walk)
