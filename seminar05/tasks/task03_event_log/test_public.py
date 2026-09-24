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
