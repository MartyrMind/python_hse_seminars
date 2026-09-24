from typing import Any

# Готовый журнал регистрации. Его очищают тесты, а не конструкторы.
registrations: list[str] = []


def register_job(name: str) -> None:
    registrations.append(name)


class Job:
    name: str

    def __init__(self, *, name: str, **kwargs: Any) -> None:
        raise NotImplementedError("Implement me")


class Timed(Job):
    timeout: int

    def __init__(self, *, timeout: int, **kwargs: Any) -> None:
        raise NotImplementedError("Implement me")


class Retried(Job):
    attempts: int

    def __init__(self, *, attempts: int, **kwargs: Any) -> None:
        raise NotImplementedError("Implement me")


class ReliableJob(Timed, Retried):
    pass


class ReverseJob(Retried, Timed):
    pass
