import inspect

import pytest

from seminar09.tasks.task05_dialogue.dialogue import RetryQuestion, dialogue

pytestmark = pytest.mark.timeout(5)


def test_two_answers_and_normal_completion() -> None:
    events: list[str] = []
    form = dialogue(events)
    assert inspect.isgenerator(form) is True
    assert events == []
    assert next(form) == "Имя?"
    assert events == ["started"]
    assert form.send("Аня") == "Город?"
    assert form.send("Москва") == "Привет, Аня из Москва!"
    assert events == ["started"]
    with pytest.raises(StopIteration) as caught:
        next(form)
    assert caught.value.value is None
    assert events == ["started", "finished"]
    form.close()
    with pytest.raises(StopIteration):
        next(form)
    assert events == ["started", "finished"]


def test_empty_strings_and_spaces_are_used_as_is() -> None:
    form = dialogue([])
    next(form)
    assert form.send("") == "Город?"
    assert form.send(" X ") == "Привет,  из  X !"
    form.close()


def test_retries_repeat_the_current_question_and_keep_the_name() -> None:
    events: list[str] = []
    form = dialogue(events)
    assert next(form) == "Имя?"
    assert form.throw(RetryQuestion()) == "Имя?"
    assert form.throw(RetryQuestion()) == "Имя?"
    assert form.send("Боря") == "Город?"
    assert form.throw(RetryQuestion()) == "Город?"
    assert form.throw(RetryQuestion()) == "Город?"
    assert form.send("Тула") == "Привет, Боря из Тула!"
    form.close()
    assert events == ["started", "finished"]


@pytest.mark.parametrize("answers", [[], ["Аня"], ["Аня", "Москва"]])
def test_close_at_each_suspension_runs_cleanup_once(answers: list[str]) -> None:
    events: list[str] = []
    form = dialogue(events)
    next(form)
    for answer in answers:
        form.send(answer)
    form.close()
    form.close()
    assert events == ["started", "finished"]
    with pytest.raises(StopIteration):
        next(form)


def test_close_before_start_does_not_run_the_body() -> None:
    events: list[str] = []
    form = dialogue(events)
    form.close()
    assert events == []
    with pytest.raises(StopIteration):
        next(form)


@pytest.mark.parametrize("answers", [[], ["Аня"], ["Аня", "Москва"]])
def test_unhandled_error_propagates_and_closes_the_form(answers: list[str]) -> None:
    events: list[str] = []
    form = dialogue(events)
    next(form)
    for answer in answers:
        form.send(answer)
    failure = RuntimeError("форма недоступна")
    with pytest.raises(RuntimeError) as caught:
        form.throw(failure)
    assert caught.value is failure
    assert events == ["started", "finished"]
    with pytest.raises(StopIteration):
        next(form)


def test_retry_after_the_greeting_is_not_caught() -> None:
    events: list[str] = []
    form = dialogue(events)
    next(form)
    form.send("Аня")
    form.send("Москва")
    failure = RetryQuestion()
    with pytest.raises(RetryQuestion) as caught:
        form.throw(failure)
    assert caught.value is failure
    assert events == ["started", "finished"]


def test_non_none_send_cannot_start_a_generator() -> None:
    events: list[str] = []
    form = dialogue(events)
    with pytest.raises(TypeError):
        form.send("слишком рано")
    assert events == []
    assert form.send(None) == "Имя?"  # type: ignore[arg-type]  # Начальный запуск.
    form.close()


def test_send_after_the_greeting_finishes_without_another_reply() -> None:
    events: list[str] = []
    form = dialogue(events)
    next(form)
    form.send("Аня")
    form.send("Москва")
    with pytest.raises(StopIteration):
        form.send("этот ответ больше не нужен")
    assert events == ["started", "finished"]
