from typing import Any

import pytest

from seminar06.tasks.task05_affine.affine import Affine


@pytest.mark.parametrize(
    ("a", "b", "x", "expected"), [(2, 1, 3, 7), (0, 8, -100, 8), (-3, 4, -2, 10)]
)
def test_call_applies_coefficients(a: int, b: int, x: int, expected: int) -> None:
    assert Affine(a, b)(x) == expected


def test_composition_order_changes_result() -> None:
    f, g = Affine(2, 1), Affine(1, 10)
    fg, gf = f * g, g * f
    assert isinstance(fg, Affine)
    assert isinstance(gf, Affine)
    assert (fg.a, fg.b, fg(3)) == (2, 21, 27)
    assert (gf.a, gf.b, gf(3)) == (2, 11, 17)


@pytest.mark.parametrize(
    ("k", "right", "left"),
    [(3, (6, 1, 25), (6, 3, 27)), (0, (0, 1, 1), (0, 0, 0)), (-2, (-4, 1, -15), (-4, -2, -18))],
)
def test_integer_scaling_depends_on_side(
    k: int, right: tuple[int, int, int], left: tuple[int, int, int]
) -> None:
    f = Affine(2, 1)
    fk, kf = f * k, k * f
    assert isinstance(fk, Affine)
    assert isinstance(kf, Affine)
    assert (fk.a, fk.b, fk(4)) == right
    assert (kf.a, kf.b, kf(4)) == left


def test_operations_create_new_objects_and_leave_operands_unchanged() -> None:
    f, g = Affine(2, 1), Affine(3, 4)
    for result in (f * g, f * 1, 1 * f, f * f):
        assert isinstance(result, Affine)
        assert result is not f and result is not g
        result.a = 99
        result.b = 99
        assert (f.a, f.b, g.a, g.b) == (2, 1, 3, 4)


def test_composed_result_keeps_its_coefficients_when_sources_change() -> None:
    f, g = Affine(2, 1), Affine(3, 4)
    result = f * g
    assert isinstance(result, Affine)
    f.a = 0
    g.b = 100
    assert (result.a, result.b, result(2)) == (6, 9, 21)


def test_chain_of_compositions() -> None:
    f, g, h = Affine(2, 1), Affine(1, 10), Affine(-1, 3)
    fg, gh = f * g, g * h
    assert isinstance(fg, Affine) and isinstance(gh, Affine)
    left, right = fg * h, f * gh
    assert isinstance(left, Affine) and isinstance(right, Affine)
    assert (left.a, left.b, left(4)) == (-2, 27, 19)
    assert (right.a, right.b, right(4)) == (-2, 27, 19)


@pytest.mark.parametrize("other", ["3", 1.5, None, [], object()])
def test_unsupported_operands_return_not_implemented(other: Any) -> None:
    f = Affine(2, 1)
    assert f.__mul__(other) is NotImplemented
    assert f.__rmul__(other) is NotImplemented
    with pytest.raises(TypeError):
        f * other
    with pytest.raises(TypeError):
        other * f


def test_not_implemented_allows_other_operand_to_handle_multiplication() -> None:
    class Receiver:
        def __rmul__(self, other: object) -> str:
            return "handled on the right"

    assert Affine(2, 1) * Receiver() == "handled on the right"
