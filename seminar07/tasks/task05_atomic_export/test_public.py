import importlib
import os
from contextlib import AbstractContextManager
from pathlib import Path
from typing import TextIO, cast

import pytest

from seminar07.tasks.task05_atomic_export.atomic_export import AtomicExport

export_module = importlib.import_module("seminar07.tasks.task05_atomic_export.atomic_export")


def as_manager(export: AtomicExport) -> AbstractContextManager[TextIO]:
    """Типизация теста: методы протокола студент добавляет к классу сам."""
    return cast(AbstractContextManager[TextIO], export)


def assert_no_temporary_files(directory: Path, target: Path) -> None:
    assert set(directory.iterdir()) == ({target} if target.exists() else set())


def test_success_replaces_report_only_after_block_and_closes_stream(tmp_path: Path) -> None:
    target = tmp_path / "report.txt"
    target.write_text("старый отчёт", encoding="utf-8")
    export = AtomicExport(target)

    with as_manager(export) as report:
        assert target.read_text(encoding="utf-8") == "старый отчёт"
        report.write("ручка;2\nкарандаш;3\n")

    assert target.read_text(encoding="utf-8") == "ручка;2\nкарандаш;3\n"
    assert report.closed
    assert export.errors == []
    assert_no_temporary_files(tmp_path, target)


def test_success_creates_missing_target_and_temp_is_in_same_directory(tmp_path: Path) -> None:
    target = tmp_path / "new.txt"
    export = AtomicExport(target)

    with as_manager(export) as report:
        report.write("товар;1\n")
        temporary_paths = list(tmp_path.iterdir())
        assert len(temporary_paths) == 1
        assert temporary_paths[0] != target
        assert temporary_paths[0].parent == target.parent
        assert not target.exists()

    assert target.read_text(encoding="utf-8") == "товар;1\n"
    assert_no_temporary_files(tmp_path, target)


def test_allowed_body_errors_are_suppressed_until_cumulative_limit(tmp_path: Path) -> None:
    target = tmp_path / "report.txt"
    target.write_text("исходный", encoding="utf-8")
    export = AtomicExport(target, allowed=(ValueError,), limit=2)
    first = ValueError("первая попытка")
    second = UnicodeError("вторая попытка")
    third = ValueError("третья попытка")

    with as_manager(export) as report:
        report.write("незавершённый 1")
        raise first
    assert target.read_text(encoding="utf-8") == "исходный"
    assert report.closed
    assert export.errors == [first]

    with as_manager(export) as report:
        report.write("успешный")
    assert target.read_text(encoding="utf-8") == "успешный"

    with as_manager(export) as report:
        report.write("незавершённый 2")
        raise second
    assert target.read_text(encoding="utf-8") == "успешный"
    assert export.errors[0] is first
    assert export.errors[1] is second

    with pytest.raises(ValueError) as caught:
        with as_manager(export) as report:
            report.write("незавершённый 3")
            raise third

    assert caught.value is third
    assert target.read_text(encoding="utf-8") == "успешный"
    assert export.errors == [first, second]
    assert_no_temporary_files(tmp_path, target)


def test_disallowed_error_does_not_spend_budget(tmp_path: Path) -> None:
    target = tmp_path / "report.txt"
    export = AtomicExport(target, allowed=(ValueError,), limit=1)
    failure = RuntimeError("неверная операция")

    with pytest.raises(RuntimeError) as caught:
        with as_manager(export) as report:
            report.write("черновик")
            raise failure

    assert caught.value is failure
    assert export.errors == []
    assert not target.exists()

    with as_manager(export) as report:
        report.write("ещё черновик")
        raise ValueError("допустимый сбой")

    assert len(export.errors) == 1
    assert not target.exists()
    assert_no_temporary_files(tmp_path, target)


@pytest.mark.parametrize("failure", [KeyboardInterrupt(), SystemExit()])
def test_process_control_error_is_not_suppressed(tmp_path: Path, failure: BaseException) -> None:
    target = tmp_path / "report.txt"
    export = AtomicExport(target, allowed=(Exception,), limit=1)

    with pytest.raises(type(failure)) as caught:
        with as_manager(export) as report:
            report.write("черновик")
            raise failure

    assert caught.value is failure
    assert export.errors == []
    assert not target.exists()
    assert_no_temporary_files(tmp_path, target)


def test_zero_and_negative_limits(tmp_path: Path) -> None:
    target = tmp_path / "report.txt"
    with pytest.raises(ValueError):
        AtomicExport(target, allowed=(ValueError,), limit=-1)

    export = AtomicExport(target, allowed=(ValueError,), limit=0)
    failure = ValueError("лимит ноль")
    with pytest.raises(ValueError) as caught:
        with as_manager(export):
            raise failure

    assert caught.value is failure
    assert export.errors == []
    assert not target.exists()
    assert_no_temporary_files(tmp_path, target)


def test_replace_failure_keeps_old_report_and_does_not_spend_budget(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    target = tmp_path / "report.txt"
    target.write_text("старый", encoding="utf-8")
    export = AtomicExport(target, allowed=(OSError,), limit=1)
    failure = PermissionError("запрещена замена")

    def fail_replace(source: os.PathLike[str] | str, dest: os.PathLike[str] | str) -> None:
        assert Path(source).parent == target.parent
        assert Path(dest) == target
        raise failure

    monkeypatch.setattr(export_module.os, "replace", fail_replace)

    with pytest.raises(PermissionError) as caught:
        with as_manager(export) as report:
            report.write("новый")

    assert caught.value is failure
    assert report.closed
    assert target.read_text(encoding="utf-8") == "старый"
    assert export.errors == []
    assert_no_temporary_files(tmp_path, target)


class CloseFailure:
    def __init__(self, wrapped: TextIO, error: BaseException) -> None:
        self.wrapped = wrapped
        self.error = error

    def write(self, text: str) -> int:
        return self.wrapped.write(text)

    def close(self) -> None:
        self.wrapped.close()
        raise self.error

    @property
    def closed(self) -> bool:
        return self.wrapped.closed


def install_close_failure(monkeypatch: pytest.MonkeyPatch, failure: BaseException) -> None:
    real_make_temp = export_module.make_temp

    def make_failing_temp(target: Path) -> tuple[Path, TextIO]:
        path, stream = real_make_temp(target)
        return path, cast(TextIO, CloseFailure(stream, failure))

    monkeypatch.setattr(export_module, "make_temp", make_failing_temp)


def test_close_failure_alone_propagates_and_keeps_old_report(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    target = tmp_path / "report.txt"
    target.write_text("старый", encoding="utf-8")
    failure = OSError("закрытие")
    install_close_failure(monkeypatch, failure)
    export = AtomicExport(target, allowed=(OSError,), limit=1)

    with pytest.raises(OSError) as caught:
        with as_manager(export) as report:
            report.write("новый")

    assert caught.value is failure
    assert report.closed
    assert target.read_text(encoding="utf-8") == "старый"
    assert export.errors == []
    assert_no_temporary_files(tmp_path, target)


def test_body_and_close_errors_are_both_kept_in_exception_group(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    target = tmp_path / "report.txt"
    target.write_text("старый", encoding="utf-8")
    body_error = ValueError("построение")
    close_error = OSError("закрытие")
    install_close_failure(monkeypatch, close_error)
    export = AtomicExport(target, allowed=(ValueError,), limit=1)

    with pytest.raises(ExceptionGroup) as caught:
        with as_manager(export) as report:
            report.write("новый")
            raise body_error

    assert caught.value.exceptions == (body_error, close_error)
    assert export.errors == []
    assert target.read_text(encoding="utf-8") == "старый"
    assert_no_temporary_files(tmp_path, target)


def test_control_error_and_close_error_use_base_exception_group(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    target = tmp_path / "report.txt"
    body_error = KeyboardInterrupt()
    close_error = OSError("закрытие")
    install_close_failure(monkeypatch, close_error)
    export = AtomicExport(target, allowed=(Exception,), limit=1)

    with pytest.raises(BaseExceptionGroup) as caught:
        with as_manager(export):
            raise body_error

    assert not isinstance(caught.value, ExceptionGroup)
    assert caught.value.exceptions == (body_error, close_error)
    assert export.errors == []
    assert not target.exists()
    assert_no_temporary_files(tmp_path, target)


def test_failure_to_create_temporary_file_leaves_target_untouched(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    target = tmp_path / "report.txt"
    target.write_text("старый", encoding="utf-8")
    failure = PermissionError("невозможно создать файл")

    def fail_create(target: Path) -> tuple[Path, TextIO]:
        raise failure

    monkeypatch.setattr(export_module, "make_temp", fail_create)
    export = AtomicExport(target, allowed=(OSError,), limit=1)

    with pytest.raises(PermissionError) as caught:
        with as_manager(export):
            pass

    assert caught.value is failure
    assert export.errors == []
    assert target.read_text(encoding="utf-8") == "старый"
    assert_no_temporary_files(tmp_path, target)
