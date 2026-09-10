from seminar01.tasks.task02_parse_build_tag.parse_build_tag import parse_build_tag


def test_normalizes_all_parts() -> None:
    assert parse_build_tag(" python / 0314 / A1B2C3D4E5 ") == (
        "PYTHON",
        314,
        "a1b2c3d",
    )


def test_keeps_only_first_seven_commit_characters() -> None:
    assert parse_build_tag("rust/42/1234567890") == ("RUST", 42, "1234567")


def test_removes_leading_zeroes_from_build_number() -> None:
    assert parse_build_tag("go/0007/ABCDEF0123") == ("GO", 7, "abcdef0")


def test_strips_whitespace_around_each_part() -> None:
    assert parse_build_tag("  kotlin\t/  12 / FedCBA987 ") == (
        "KOTLIN",
        12,
        "fedcba9",
    )
