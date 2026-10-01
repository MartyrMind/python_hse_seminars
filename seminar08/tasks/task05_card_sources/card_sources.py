from abc import ABC


class CardSource(ABC):  # noqa: B024 — абстрактные методы добавляет студент
    """Общий интерфейс источника карточек."""


class StackSource(CardSource):
    """Выдаёт последнюю добавленную карточку."""


class QueueSource(CardSource):
    """Выдаёт первую добавленную карточку."""
