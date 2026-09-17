import pytest

from seminar03.tasks.task03_group_events.group_events import Event, group_events


@pytest.mark.timeout(3)
def test_many_event_kinds_finish_in_time() -> None:
    events: list[Event] = [(f"kind-{index:05d}", f"message-{index:05d}") for index in range(60_000)]

    result = group_events(events)

    assert len(result) == 60_000
    assert result["kind-00000"] == ["message-00000"]
    assert result["kind-59999"] == ["message-59999"]
