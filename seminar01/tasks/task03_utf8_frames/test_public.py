from seminar01.tasks.task03_utf8_frames.utf8_frames import utf8_frames


def test_ascii_text_needs_two_frames() -> None:
    assert utf8_frames("hello", 4) == (5, 5, 2, 3)


def test_cyrillic_uses_two_bytes_per_character() -> None:
    assert utf8_frames("привет", 4) == (6, 12, 3, 0)


def test_emoji_uses_four_utf8_bytes() -> None:
    assert utf8_frames("A🙂", 4) == (2, 5, 2, 3)


def test_exact_boundary_has_no_unused_bytes() -> None:
    assert utf8_frames("abcdefgh", 4) == (8, 8, 2, 0)


def test_empty_text_needs_no_frames() -> None:
    assert utf8_frames("", 4) == (0, 0, 0, 0)
