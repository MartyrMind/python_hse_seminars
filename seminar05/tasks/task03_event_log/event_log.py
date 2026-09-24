class EventLog:
    prefix: str = "INFO"

    def __init__(self, initial: list[str] | None = None) -> None:
        raise NotImplementedError("Implement me")

    def add(self, message: str) -> str:
        """Сформировать запись с текущим prefix, сохранить и вернуть её."""
        raise NotImplementedError("Implement me")

    def snapshot(self) -> list[str]:
        """Вернуть отдельный список уже сформированных записей."""
        raise NotImplementedError("Implement me")
