from seminar03.tasks.task03_group_events.group_events import Event, group_events


def test_groups_messages_by_kind() -> None:
    events: list[Event] = [
        ("info", "started"),
        ("error", "timeout"),
        ("info", "finished"),
    ]
    assert group_events(events) == {
        "info": ["started", "finished"],
        "error": ["timeout"],
    }


def test_preserves_message_order_and_repetitions() -> None:
    events: list[Event] = [
        ("warning", "disk"),
        ("warning", "memory"),
        ("warning", "disk"),
    ]
    assert group_events(events) == {"warning": ["disk", "memory", "disk"]}


def test_keys_follow_first_appearance() -> None:
    events: list[Event] = [("z", "one"), ("a", "two"), ("z", "three"), ("m", "four")]
    assert list(group_events(events)) == ["z", "a", "m"]


def test_empty_input_produces_empty_dictionary() -> None:
    assert group_events([]) == {}


def test_result_lists_are_independent() -> None:
    grouped = group_events([("a", "same"), ("b", "same")])
    grouped["a"].append("extra")
    assert grouped["b"] == ["same"]


def test_does_not_change_input() -> None:
    events: list[Event] = [("info", "started"), ("error", "timeout")]
    group_events(events)
    assert events == [("info", "started"), ("error", "timeout")]
