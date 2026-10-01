import pytest

from seminar07.tasks.task02_load_pages.load_pages import Page, PageLoadError, load_pages


def test_primary_loads_all_pages_and_saves_once() -> None:
    calls: list[tuple[str, str | None]] = []
    saved: list[list[str]] = []
    pages = {
        None: Page(["ручка;2", "ластик;1"], "c1"),
        "c1": Page([], "c2"),
        "c2": Page(["карандаш;3"], None),
    }

    def primary(cursor: str | None) -> Page:
        calls.append(("primary", cursor))
        return pages[cursor]

    def reserve(cursor: str | None) -> Page:
        calls.append(("reserve", cursor))
        raise AssertionError("Резерв не нужен")

    def save_all(rows: list[str]) -> None:
        calls.append(("save", None))
        saved.append(rows.copy())

    result = load_pages(3, None, primary, reserve, save_all)

    assert result == ["ручка;2", "ластик;1", "карандаш;3"]
    assert saved == [result]
    assert calls == [
        ("primary", None),
        ("primary", "c1"),
        ("primary", "c2"),
        ("save", None),
    ]


def test_failover_retries_same_cursor_and_stays_on_reserve() -> None:
    calls: list[tuple[str, str | None]] = []
    saved: list[list[str]] = []

    def primary(cursor: str | None) -> Page:
        calls.append(("primary", cursor))
        if cursor == "c1":
            raise TimeoutError("основной узел не ответил")
        return Page(["ручка;2"], "c1")

    def reserve(cursor: str | None) -> Page:
        calls.append(("reserve", cursor))
        if cursor == "c1":
            return Page(["карандаш;3"], "c2")
        return Page(["линейка;1"], None)

    result = load_pages(3, None, primary, reserve, lambda rows: saved.append(rows.copy()))

    assert result == ["ручка;2", "карандаш;3", "линейка;1"]
    assert saved == [result]
    assert calls == [
        ("primary", None),
        ("primary", "c1"),
        ("reserve", "c1"),
        ("reserve", "c2"),
    ]


@pytest.mark.parametrize("error", [ConnectionResetError("сброс"), ConnectionRefusedError("отказ")])
def test_connection_error_subclasses_trigger_failover(error: ConnectionError) -> None:
    calls: list[str] = []

    def primary(cursor: str | None) -> Page:
        calls.append("primary")
        raise error

    def reserve(cursor: str | None) -> Page:
        calls.append("reserve")
        return Page(["ручка;2"], None)

    result = load_pages(1, "start", primary, reserve, lambda rows: calls.append("save"))

    assert result == ["ручка;2"]
    assert calls == ["primary", "reserve", "save"]


@pytest.mark.parametrize("error", [ValueError("формат"), FileNotFoundError("файл")])
def test_other_primary_errors_are_wrapped_without_failover(error: Exception) -> None:
    calls: list[str] = []

    def primary(cursor: str | None) -> Page:
        calls.append("primary")
        raise error

    def reserve(cursor: str | None) -> Page:
        calls.append("reserve")
        return Page([], None)

    with pytest.raises(PageLoadError) as caught:
        load_pages(2, "start", primary, reserve, lambda rows: calls.append("save"))

    assert caught.value.__cause__ is error
    assert (caught.value.source, caught.value.page_number, caught.value.cursor) == (
        "primary",
        1,
        "start",
    )
    assert calls == ["primary"]


@pytest.mark.parametrize("error", [TimeoutError("таймаут"), ValueError("формат")])
def test_reserve_errors_are_wrapped_and_no_rows_are_saved(error: Exception) -> None:
    calls: list[tuple[str, str | None]] = []

    def primary(cursor: str | None) -> Page:
        calls.append(("primary", cursor))
        if cursor == "c1":
            raise ConnectionError("сеть")
        return Page(["ручка;2"], "c1")

    def reserve(cursor: str | None) -> Page:
        calls.append(("reserve", cursor))
        raise error

    with pytest.raises(PageLoadError) as caught:
        load_pages(2, None, primary, reserve, lambda rows: calls.append(("save", None)))

    assert caught.value.__cause__ is error
    assert (caught.value.source, caught.value.page_number, caught.value.cursor) == (
        "reserve",
        2,
        "c1",
    )
    assert calls == [("primary", None), ("primary", "c1"), ("reserve", "c1")]


def test_reserve_failure_on_later_page_is_wrapped() -> None:
    calls: list[tuple[str, str | None]] = []

    def primary(cursor: str | None) -> Page:
        calls.append(("primary", cursor))
        raise ConnectionError("сеть")

    failure = OSError("резерв недоступен")

    def reserve(cursor: str | None) -> Page:
        calls.append(("reserve", cursor))
        if cursor is None:
            return Page(["ручка;2"], "c1")
        raise failure

    with pytest.raises(PageLoadError) as caught:
        load_pages(2, None, primary, reserve, lambda rows: calls.append(("save", None)))

    assert caught.value.__cause__ is failure
    assert (caught.value.source, caught.value.page_number, caught.value.cursor) == (
        "reserve",
        2,
        "c1",
    )
    assert calls == [("primary", None), ("reserve", None), ("reserve", "c1")]


def test_early_end_raises_without_saving() -> None:
    calls: list[str] = []

    def primary(cursor: str | None) -> Page:
        calls.append("primary")
        return Page(["ручка;2"], None)

    with pytest.raises(PageLoadError) as caught:
        load_pages(
            2, "start", primary, lambda cursor: Page([], None), lambda rows: calls.append("save")
        )

    assert caught.value.__cause__ is None
    assert (caught.value.source, caught.value.page_number, caught.value.cursor) == (
        "primary",
        1,
        "start",
    )
    assert calls == ["primary"]


def test_nonpositive_page_count_calls_nothing() -> None:
    calls: list[str] = []

    def fetch(cursor: str | None) -> Page:
        calls.append("fetch")
        return Page([], None)

    with pytest.raises(ValueError):
        load_pages(0, None, fetch, fetch, lambda rows: calls.append("save"))

    assert calls == []


def test_saver_error_propagates_unchanged() -> None:
    failure = RuntimeError("диск")
    calls: list[str] = []

    def primary(cursor: str | None) -> Page:
        calls.append("primary")
        return Page(["ручка;2"], None)

    def save_all(rows: list[str]) -> None:
        calls.append("save")
        assert rows == ["ручка;2"]
        raise failure

    with pytest.raises(RuntimeError) as caught:
        load_pages(1, None, primary, lambda cursor: Page([], None), save_all)

    assert caught.value is failure
    assert calls == ["primary", "save"]


@pytest.mark.parametrize("error", [KeyboardInterrupt(), SystemExit()])
def test_process_control_exceptions_propagate(error: BaseException) -> None:
    calls: list[str] = []

    def primary(cursor: str | None) -> Page:
        calls.append("primary")
        raise error

    with pytest.raises(type(error)) as caught:
        load_pages(
            1, None, primary, lambda cursor: Page([], None), lambda rows: calls.append("save")
        )

    assert caught.value is error
    assert calls == ["primary"]
