from collections.abc import Iterator

import pytest

from seminar06.tasks.task06_cooperative_job.cooperative_job import (
    Job,
    ReliableJob,
    Retried,
    ReverseJob,
    Timed,
    registrations,
)


@pytest.fixture(autouse=True)
def clear_registrations() -> Iterator[None]:
    registrations.clear()
    yield
    registrations.clear()


def test_base_job_registers_once() -> None:
    job = Job(name="base")
    assert job.name == "base"
    assert registrations == ["base"]


def test_individual_features_work_without_each_other() -> None:
    timed = Timed(name="timer", timeout=5)
    retried = Retried(name="retry", attempts=3)
    assert (timed.name, timed.timeout) == ("timer", 5)
    assert (retried.name, retried.attempts) == ("retry", 3)
    assert registrations == ["timer", "retry"]


@pytest.mark.parametrize("cls", [ReliableJob, ReverseJob])
def test_both_base_orders_initialize_all_fields_and_register_once(
    cls: type[ReliableJob] | type[ReverseJob],
) -> None:
    job = cls(name="download", timeout=5, attempts=3)
    assert (job.name, job.timeout, job.attempts) == ("download", 5, 3)
    assert registrations == ["download"]


def test_multiple_objects_keep_independent_fields_and_all_registrations() -> None:
    first = ReliableJob(name="same", timeout=5, attempts=3)
    second = ReverseJob(name="same", timeout=10, attempts=1)
    first.timeout = 99
    assert (second.name, second.timeout, second.attempts) == ("same", 10, 1)
    assert registrations == ["same", "same"]


def test_keyword_argument_order_does_not_matter() -> None:
    job = ReverseJob(attempts=2, name="upload", timeout=8)
    assert (job.name, job.timeout, job.attempts) == ("upload", 8, 2)
    assert registrations == ["upload"]
