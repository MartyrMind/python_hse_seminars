from typing import Any

registrations: list[str] = []


def register_job(name: str) -> None:
    registrations.append(name)


class Job:
    name: str

    def __init__(self, **options: Any) -> None:
        raise NotImplementedError("Implement me")


class Timed(Job):
    timeout: int


class Retried(Job):
    attempts: int


class ReliableJob(Timed, Retried):
    pass


class ReverseJob(Retried, Timed):
    pass
