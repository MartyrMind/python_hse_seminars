import inspect
from collections.abc import Generator

import pytest

from seminar09.tasks.task06_relay.relay import relay

pytestmark = pytest.mark.timeout(5)


def test_send_reaches_worker_and_return_value_is_preserved() -> None:
    events: list[str] = []

    def worker() -> Generator[str, str, int]:
        events.append("worker:started")
        try:
            answer = yield "вопрос"
            yield f"ответ:{answer}"
            return 42
        finally:
            events.append("worker:finished")

    inner = worker()
    walk = relay(inner, events)
    assert inspect.isgenerator(walk) is True
    assert events == []
    assert next(walk) == "вопрос"
    assert events == ["started", "worker:started"]
    assert walk.send("да") == "ответ:да"
    assert events == ["started", "worker:started"]
    with pytest.raises(StopIteration) as caught:
        next(walk)
    assert caught.value.value == 42
    assert events == ["started", "worker:started", "worker:finished", "finished"]
    with pytest.raises(StopIteration):
        next(walk)
    walk.close()
    assert events.count("finished") == 1


def test_handled_throw_returns_workers_next_yield_and_keeps_running() -> None:
    events: list[str] = []
    failure = ValueError("повтор")

    def worker() -> Generator[str, str, str]:
        try:
            yield "ожидание"
        except ValueError as error:
            assert error is failure
            answer = yield "восстановлен"
            return answer
        return "без ошибки"

    inner = worker()
    walk = relay(inner, events)
    assert next(walk) == "ожидание"
    assert walk.throw(failure) == "восстановлен"
    assert events == ["started"]
    with pytest.raises(StopIteration) as caught:
        walk.send("продолжили")
    assert caught.value.value == "продолжили"
    assert events == ["started", "finished"]


def test_unhandled_throw_propagates_and_runs_both_finally_blocks() -> None:
    events: list[str] = []

    def worker() -> Generator[int]:
        try:
            yield 1
        finally:
            events.append("worker:finished")

    inner = worker()
    walk = relay(inner, events)
    next(walk)
    failure = RuntimeError("отмена")
    with pytest.raises(RuntimeError) as caught:
        walk.throw(failure)
    assert caught.value is failure
    assert events == ["started", "worker:finished", "finished"]
    assert inspect.getgeneratorstate(inner) == inspect.GEN_CLOSED


def test_close_explicitly_closes_the_retained_worker() -> None:
    events: list[str] = []

    def worker() -> Generator[int]:
        try:
            yield 1
            yield 2
        finally:
            events.append("worker:finished")

    inner = worker()  # Сохраняем ссылку: сборка мусора не должна закрыть его за relay.
    walk = relay(inner, events)
    assert next(walk) == 1
    walk.close()
    assert events == ["started", "worker:finished", "finished"]
    assert inspect.getgeneratorstate(inner) == inspect.GEN_CLOSED
    walk.close()
    assert events == ["started", "worker:finished", "finished"]
    with pytest.raises(StopIteration):
        next(walk)


def test_unstarted_close_leaves_worker_unstarted() -> None:
    events: list[str] = []

    def worker() -> Generator[int]:
        try:
            events.append("worker:started")
            yield 1
        finally:
            events.append("worker:finished")

    inner = worker()
    walk = relay(inner, events)
    walk.close()
    assert events == []
    assert inspect.getgeneratorstate(inner) == inspect.GEN_CREATED
    with pytest.raises(StopIteration):
        next(walk)
    inner.close()
    assert events == []


def test_worker_can_return_without_yielding_anything() -> None:
    def worker() -> Generator[int, None, str]:
        yield from ()
        return "пустой результат"

    events: list[str] = []
    walk = relay(worker(), events)
    with pytest.raises(StopIteration) as caught:
        next(walk)
    assert caught.value.value == "пустой результат"
    assert events == ["started", "finished"]


def test_error_before_first_worker_yield_runs_outer_cleanup() -> None:
    failure = LookupError("не удалось начать")

    def worker() -> Generator[int]:
        raise failure
        yield 1

    events: list[str] = []
    walk = relay(worker(), events)
    with pytest.raises(LookupError) as caught:
        next(walk)
    assert caught.value is failure
    assert events == ["started", "finished"]


def test_generator_exit_reaches_worker() -> None:
    events: list[str] = []

    def worker() -> Generator[int]:
        try:
            yield 1
        except GeneratorExit:
            events.append("worker:exit")
            raise
        finally:
            events.append("worker:finished")

    inner = worker()
    walk = relay(inner, events)
    next(walk)
    walk.close()
    assert events == ["started", "worker:exit", "worker:finished", "finished"]


def test_failure_during_worker_close_still_runs_outer_cleanup() -> None:
    events: list[str] = []
    failure = RuntimeError("ошибка очистки")

    def worker() -> Generator[int]:
        try:
            yield 1
        finally:
            events.append("worker:finished")
            raise failure

    inner = worker()
    walk = relay(inner, events)
    next(walk)
    with pytest.raises(RuntimeError) as caught:
        walk.close()
    assert caught.value is failure
    assert events == ["started", "worker:finished", "finished"]
    assert inspect.getgeneratorstate(inner) == inspect.GEN_CLOSED
    assert inspect.getgeneratorstate(walk) == inspect.GEN_CLOSED
