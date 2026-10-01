from collections.abc import Iterable


class Deck:
    """Готовый класс из внешней библиотеки. Не изменяйте его определение."""

    def __init__(self, cards: Iterable[str]) -> None:
        self._cards = list(cards)

    def __len__(self) -> int:
        return len(self._cards)

    def __getitem__(self, index: int) -> str:
        return self._cards[index]


def enable_shuffle() -> None:
    raise NotImplementedError("Implement me")
