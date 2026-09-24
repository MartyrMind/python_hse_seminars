from typing import Any

from seminar05.tasks.task05_task_queue.task_queue import TaskQueue


def test_submit_is_deferred_and_run_preserves_order_and_none_results() -> None:
    queue = TaskQueue()
    events: list[str] = []
    ticket = queue.submit(events.append, "one")
    assert ticket.ready is False
    assert ticket.value is None
    queue.submit(events.append, "two")
    queue.submit(len, events)
    assert events == []
    assert queue.run_all() == [None, None, 2]
    assert ticket.ready is True
    assert ticket.value is None
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


def test_result_can_be_used_in_later_positional_and_keyword_arguments() -> None:
    def add(x: int, *, y: int) -> int:
        return x + y

    queue = TaskQueue()
    first = queue.submit(int, "7")
    second = queue.submit(add, first, y=first)
    third = queue.submit(str, second)
    assert first is not second and second is not third
    assert [first.ready, second.ready, third.ready] == [False, False, False]
    assert queue.run_all() == [7, 14, "14"]
    assert [first.value, second.value, third.value] == [7, 14, "14"]
    assert [first.ready, second.ready, third.ready] == [True, True, True]


def test_none_result_is_ready_and_can_be_passed_on() -> None:
    events: list[int] = []
    queue = TaskQueue()
    first = queue.submit(events.append, 1)
    second = queue.submit(str, first)
    assert queue.run_all() == [None, "None"]
    assert first.ready is True and first.value is None
    assert second.value == "None"


def test_result_is_ready_before_the_next_callback_runs() -> None:
    queue = TaskQueue()
    first = queue.submit(int, "7")

    def observe() -> tuple[bool, int, bool]:
        return first.ready, first.value, second.ready

    second = queue.submit(observe)
    assert queue.run_all() == [7, (True, 7, False)]
    assert second.ready is True


def test_result_from_previous_run_preserves_identity_and_current_mutable_value() -> None:
    queue = TaskQueue()
    first = queue.submit(list)
    results = queue.run_all()
    assert first.value is results[0]
    first.value.append(7)
    second = queue.submit(len, first)
    assert queue.run_all() == [1]
    assert first.value == [7] and second.value == 1


def test_result_of_new_task_stays_pending_until_next_run() -> None:
    queue = TaskQueue()
    earlier = queue.submit(int, "4")

    def schedule() -> Any:
        return queue.submit(str, earlier)

    scheduled = queue.submit(schedule)
    results = queue.run_all()
    new_ticket = scheduled.value
    assert results[0] == 4
    assert results[1] is new_ticket
    assert scheduled.ready is True
    assert new_ticket.ready is False and new_ticket.value is None
    assert queue.run_all() == ["4"]
    assert new_ticket.ready is True and new_ticket.value == "4"


def test_binding_does_not_replace_saved_result_objects_with_their_values() -> None:
    queue = TaskQueue()
    first = queue.submit(int, "5")
    options = {"x": first}

    def record(**kwargs: Any) -> dict[str, Any]:
        return kwargs

    second = queue.submit(record, **options)
    assert queue.run_all() == [5, {"x": 5}]
    assert options["x"] is first
    assert second.value == {"x": 5}


def test_result_substitution_happens_only_once() -> None:
    queue = TaskQueue()

    def schedule() -> Any:
        return queue.submit(str, 42)

    scheduled = queue.submit(schedule)

    def observe(positional: Any, *, named: Any) -> str:
        assert positional is scheduled.value
        assert named is scheduled.value
        assert positional.ready is False
        return "observed"

    observed = queue.submit(observe, scheduled, named=scheduled)
    results = queue.run_all()
    assert results[0] is scheduled.value
    assert results[1] == observed.value == "observed"
    assert queue.run_all() == ["42"]
