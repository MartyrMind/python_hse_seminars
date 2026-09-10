from seminar01.tasks.task05_decode_access_card.decode_access_card import decode_access_card


def test_active_card_with_middle_access_level() -> None:
    assert decode_access_card(" ami / 0042 / A5 ") == ("AMI", 42, True, 2)


def test_inactive_card_with_maximum_access_level() -> None:
    assert decode_access_card("rnd/0007/0E") == ("RND", 7, False, 7)


def test_active_card_with_zero_access_level() -> None:
    assert decode_access_card("ops/0001/01") == ("OPS", 1, True, 0)


def test_hexadecimal_digits_are_case_insensitive() -> None:
    assert decode_access_card("lab/0015/0f") == ("LAB", 15, True, 7)
