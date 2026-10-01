import os
import subprocess
import sys
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest

from seminar08.tasks.task06_repeat_to_length.fragments import BeatFragment, TextFragment
from seminar08.tasks.task06_repeat_to_length.repeat_to_length import (
    RepeatLengthError,
    repeat_all,
    repeat_to_length,
)


@pytest.mark.parametrize(
    ("value", "minimum", "expected"),
    [("ab", 5, "ababab"), ("abc", 3, "abc"), ("z", 4, "zzzz")],
)
def test_repeats_the_fewest_times_needed(value: str, minimum: int, expected: str) -> None:
    assert repeat_to_length(value, minimum) == expected


def test_foreign_fragment_types_are_preserved() -> None:
    text = repeat_to_length(TextFragment("ab"), 5)
    beats = repeat_to_length(BeatFragment(("kick", "snare")), 5)

    assert text == TextFragment("ababab")
    assert isinstance(text, TextFragment)
    assert beats == BeatFragment(("kick", "snare") * 3)
    assert isinstance(beats, BeatFragment)


def test_repeat_all_accepts_generator_and_preserves_order() -> None:
    source = (TextFragment(text) for text in ["ab", "xyz"])

    assert repeat_all(source, 5) == [TextFragment("ababab"), TextFragment("xyzxyz")]
    assert repeat_all([], 5) == []


@pytest.mark.parametrize("minimum", [0, -1])
def test_nonpositive_minimum_is_rejected_even_for_empty_batch(minimum: int) -> None:
    with pytest.raises(ValueError):
        repeat_to_length("a", minimum)
    with pytest.raises(ValueError):
        repeat_all([], minimum)


def test_empty_fragment_is_rejected() -> None:
    with pytest.raises(ValueError):
        repeat_to_length("", 1)


def test_wrong_result_length_raises_detailed_error() -> None:
    class DropsOne:
        def __init__(self, text: str) -> None:
            self.text = text

        def __len__(self) -> int:
            return len(self.text)

        def __mul__(self, copies: int) -> DropsOne:
            return DropsOne((self.text * copies)[:-1])

    with pytest.raises(RepeatLengthError) as caught:
        repeat_to_length(DropsOne("ab"), 5)

    error: Any = caught.value
    assert (error.copies, error.expected_length, error.actual_length) == (3, 6, 5)


def test_batch_stops_at_first_length_violation() -> None:
    seen: list[str] = []

    class Broken:
        def __len__(self) -> int:
            return 2

        def __mul__(self, copies: int) -> Broken:
            return Broken()

    def source() -> Iterator[Any]:
        seen.append("first")
        yield TextFragment("a")
        seen.append("broken")
        yield Broken()
        seen.append("unreached")
        yield TextFragment("z")

    with pytest.raises(RepeatLengthError):
        repeat_all(source(), 5)

    assert seen == ["first", "broken"]


def test_error_from_multiplication_propagates_unchanged() -> None:
    failure = RuntimeError("умножение сломалось")

    class Broken:
        def __len__(self) -> int:
            return 2

        def __mul__(self, copies: int) -> Broken:
            raise failure

    with pytest.raises(RuntimeError) as caught:
        repeat_to_length(Broken(), 5)
    assert caught.value is failure


def test_error_from_result_length_propagates_unchanged() -> None:
    failure = TypeError("длина сломалась")

    class Broken:
        def __init__(self, bad: bool = False) -> None:
            self.bad = bad

        def __len__(self) -> int:
            if self.bad:
                raise failure
            return 2

        def __mul__(self, copies: int) -> Broken:
            return Broken(bad=True)

    with pytest.raises(TypeError) as caught:
        repeat_to_length(Broken(), 5)
    assert caught.value is failure


def _check_mypy(tmp_path: Path, source: str) -> subprocess.CompletedProcess[str]:
    root = Path(__file__).resolve().parents[3]
    snippet = tmp_path / "typing_case.py"
    snippet.write_text(source, encoding="utf-8")
    env = os.environ.copy()
    env["MYPYPATH"] = str(root) + os.pathsep + env.get("MYPYPATH", "")
    return subprocess.run(
        [sys.executable, "-m", "mypy", "--strict", "--no-incremental", str(snippet)],
        cwd=root,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


def test_static_types_keep_concrete_result_type(tmp_path: Path) -> None:
    result = _check_mypy(
        tmp_path,
        """from typing import assert_type
from seminar08.tasks.task06_repeat_to_length.fragments import BeatFragment, TextFragment
from seminar08.tasks.task06_repeat_to_length.repeat_to_length import repeat_all, repeat_to_length

assert_type(repeat_to_length("ab", 5), str)
assert_type(repeat_to_length(TextFragment("ab"), 5), TextFragment)
assert_type(repeat_all((BeatFragment(("kick",)) for _ in range(2)), 3), list[BeatFragment])
""",
    )

    assert result.returncode == 0, result.stdout + result.stderr


def test_static_types_reject_missing_or_wrong_operations(tmp_path: Path) -> None:
    result = _check_mypy(
        tmp_path,
        """from typing import Self
from seminar08.tasks.task06_repeat_to_length.repeat_to_length import repeat_to_length

class NoLength:
    def __mul__(self, copies: int) -> Self:
        return self

class WrongMultiply:
    def __len__(self) -> int:
        return 1
    def __mul__(self, copies: int) -> str:
        return "x"

repeat_to_length(NoLength(), 3)
repeat_to_length(WrongMultiply(), 3)
""",
    )

    assert result.returncode != 0
    assert "NoLength" in result.stdout
    assert "WrongMultiply" in result.stdout
