from collections.abc import Generator


class RetryQuestion(Exception):
    """Повторить вопрос, на котором приостановлен диалог."""


def dialogue(events: list[str]) -> Generator[str, str, None]:  # noqa: UP043
    raise NotImplementedError("Implement me")
