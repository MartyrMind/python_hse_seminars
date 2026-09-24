from collections.abc import Callable
from typing import Any

from seminar05.tasks.task05_task_queue.task_queue import TaskQueue


def test_submit_is_deferred_and_run_preserves_order_and_none_results() -> None:
    queue = TaskQueue()
    events: list[str] = []
    submit: Callable[..., object] = queue.submit
    assert submit(events.append, "one") is None
    queue.submit(events.append, "two")
    queue.submit(len, events)
    assert events == []
    assert queue.run_all() == [None, None, 2]
    assert events == ["one", "two"]
    assert queue.run_all() == []


def test_forwards_keyword_names_that_match_queue_parameters() -> None:
    def payload(**values: Any) -> dict[str, Any]:
        return values

    queue = TaskQueue()
    queue.submit(payload, func="f", self="s", args=1, kwargs=2)
    assert queue.run_all() == [{"func": "f", "self": "s", "args": 1, "kwargs": 2}]


def test_stores_argument_references_but_keyword_mapping_is_already_unpacked() -> None:
    values = [1]
    options: dict[str, Any] = {"items": values}

    def identity(*, items: list[int]) -> list[int]:
        return items

    queue = TaskQueue()
    queue.submit(identity, **options)
    options["items"] = [99]
    values.append(2)
    results = queue.run_all()
    assert results[0] is values
    assert results == [[1, 2]]


def test_saved_method_uses_original_instance_and_current_state() -> None:
    class Counter:
        def __init__(self, value: int) -> None:
            self.value = value

        def add(self, amount: int) -> int:
            self.value += amount
            return self.value

    first, second = Counter(0), Counter(100)
    queue = TaskQueue()
    queue.submit(first.add, 1)
    queue.submit(second.add, 2)
    first.value = 10
    assert queue.run_all() == [11, 102]
    assert (first.value, second.value) == (11, 102)


def test_new_tasks_added_during_run_wait_until_next_run() -> None:
    queue = TaskQueue()
    events: list[str] = []

    def schedule() -> str:
        events.append("schedule")
        queue.submit(events.append, "later")
        return "scheduled"

    queue.submit(schedule)
    queue.submit(events.append, "already queued")
    assert queue.run_all() == ["scheduled", None]
    assert events == ["schedule", "already queued"]
    assert queue.run_all() == [None]
    assert events == ["schedule", "already queued", "later"]
    assert queue.run_all() == []


def test_queues_and_repeated_runs_are_independent() -> None:
    first, second = TaskQueue(), TaskQueue()
    first.submit(str, 1)
    assert second.run_all() == []
    assert first.run_all() == ["1"]
    first.submit(str, 2)
    second.submit(str, 3)
    assert first.run_all() == ["2"]
    assert second.run_all() == ["3"]
