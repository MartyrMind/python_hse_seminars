from seminar02.tasks.task01_delivery_quote.delivery_quote import delivery_quote


def test_light_parcel_uses_first_tariff() -> None:
    assert delivery_quote(0.5, False) == "Доставка: 200.00 ₽"


def test_one_kilogram_is_in_first_tariff() -> None:
    assert delivery_quote(1.0, False) == "Доставка: 200.00 ₽"


def test_five_kilograms_is_in_second_tariff() -> None:
    assert delivery_quote(5.0, False) == "Доставка: 350.00 ₽"


def test_heavy_parcel_pays_for_extra_weight() -> None:
    assert delivery_quote(7.0, False) == "Доставка: 450.00 ₽"


def test_express_delivery_increases_final_price() -> None:
    assert delivery_quote(7.0, True) == "Доставка: 675.00 ₽"
