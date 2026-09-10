from seminar01.tasks.task06_bonus_mass_to_grams.mass_to_grams import mass_to_grams


def test_comma_separator_and_thousands_spaces() -> None:
    assert mass_to_grams("1 234,056") == 1_234_056


def test_dot_separator() -> None:
    assert mass_to_grams("12.500") == 12_500


def test_leading_zeroes_do_not_change_value() -> None:
    assert mass_to_grams("0007,005") == 7_005


def test_zero() -> None:
    assert mass_to_grams("0,000") == 0
