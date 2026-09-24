import pytest

from seminar05.tasks.task03_event_log.event_log import EventLog


def test_default_prefix_and_independent_instance_lists() -> None:
    first, second = EventLog(), EventLog()
    assert first.add("started") == "[INFO] started"
    assert first.snapshot() == ["[INFO] started"]
    assert second.snapshot() == []


@pytest.mark.parametrize("initial", [[], ["old"]])
def test_constructor_copies_initial_list(initial: list[str]) -> None:
    original = initial.copy()
    log = EventLog(initial)
    initial.append("outside")
    assert log.snapshot() == original
    log.add("inside")
    assert initial == original + ["outside"]


def test_snapshot_is_independent_in_both_directions() -> None:
    log = EventLog(["old"])
    saved = log.snapshot()
    saved.append("outside")
    assert log.snapshot() == ["old"]
    log.add("new")
    assert saved == ["old", "outside"]


def test_class_prefix_change_affects_existing_and_new_instances(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    log = EventLog()
    log.add("before")
    monkeypatch.setattr(EventLog, "prefix", "DEBUG")
    assert log.add("after") == "[DEBUG] after"
    assert EventLog().add("new") == "[DEBUG] new"
    assert log.snapshot() == ["[INFO] before", "[DEBUG] after"]


def test_instance_prefix_shadows_class_without_changing_other_instances(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    local, shared = EventLog(), EventLog()
    local.prefix = "LOCAL"
    monkeypatch.setattr(EventLog, "prefix", "GLOBAL")
    assert local.add("one") == "[LOCAL] one"
    assert shared.add("two") == "[GLOBAL] two"
    assert EventLog.prefix == "GLOBAL"


def test_saved_bound_method_reads_current_instance_state() -> None:
    log = EventLog()
    add = log.add
    log.prefix = "LATER"
    assert add("") == "[LATER] "
    assert EventLog.add(log, "direct") == "[LATER] direct"
    assert log.snapshot() == ["[LATER] ", "[LATER] direct"]


def test_empty_prefix_is_an_individual_setting() -> None:
    log = EventLog()
    log.prefix = ""
    assert log.add("") == "[] "
    assert log.snapshot() == ["[] "]


def test_fork_copies_history_and_both_logs_can_continue_independently() -> None:
    original = EventLog(["old"])
    original.add("before")
    forked = original.fork()
    assert forked is not original
    assert forked.snapshot() == ["old", "[INFO] before"]
    original.add("left")
    forked.add("right")
    assert original.snapshot() == ["old", "[INFO] before", "[INFO] left"]
    assert forked.snapshot() == ["old", "[INFO] before", "[INFO] right"]


def test_fork_of_shared_prefix_still_follows_class_setting(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original = EventLog()
    forked = original.fork()
    monkeypatch.setattr(EventLog, "prefix", "DEBUG")
    assert original.add("a") == "[DEBUG] a"
    assert forked.add("b") == "[DEBUG] b"
    original.prefix = "LOCAL"
    assert forked.add("c") == "[DEBUG] c"


def test_fork_keeps_personal_prefix_even_when_equal_to_class_setting(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original = EventLog()
    original.prefix = "INFO"
    forked = original.fork()
    monkeypatch.setattr(EventLog, "prefix", "DEBUG")
    assert original.add("a") == "[INFO] a"
    assert forked.add("b") == "[INFO] b"
    forked.prefix = "FORK"
    assert original.add("c") == "[INFO] c"
    assert forked.add("d") == "[FORK] d"


def test_fork_of_fork_preserves_empty_personal_prefix(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original = EventLog()
    original.prefix = ""
    forked = original.fork().fork()
    monkeypatch.setattr(EventLog, "prefix", "ERROR")
    assert forked.add("") == "[] "
    assert original.snapshot() == []
