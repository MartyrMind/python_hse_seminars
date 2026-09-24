import pytest

from seminar06.tasks.task01_message_factory.message_factory import (
    LoudMessage,
    Message,
    QuotedMessage,
)


@pytest.mark.parametrize(
    ("cls", "expected"),
    [(Message, "привет"), (LoudMessage, "ПРИВЕТ"), (QuotedMessage, "«привет»")],
)
def test_factory_preserves_class_and_uses_its_renderer(cls: type[Message], expected: str) -> None:
    message = cls.from_line(" \tпривет\n")
    assert type(message) is cls
    assert message.render() == expected


@pytest.mark.parametrize("text", ["", " \t\n"])
def test_empty_text_is_allowed(text: str) -> None:
    assert QuotedMessage.from_line(text).render() == "«»"


def test_internal_whitespace_is_preserved() -> None:
    assert Message.from_line("  два  слова \n").text == "два  слова"


def test_new_descendant_uses_inherited_factory_and_its_constructor() -> None:
    class TaggedMessage(LoudMessage):
        def __init__(self, text: str) -> None:
            super().__init__(text)
            self.tag = "new"

    message = TaggedMessage.from_line("  текст  ")
    assert type(message) is TaggedMessage
    assert message.tag == "new"
    assert message.render() == "ТЕКСТ"


def test_factory_called_through_instance_creates_a_new_object() -> None:
    original = QuotedMessage("старое")
    result = original.from_line(" новое ")
    assert type(result) is QuotedMessage
    assert result is not original
    assert result.render() == "«новое»"
    assert original.text == "старое"


def test_repeated_calls_create_independent_messages() -> None:
    first = Message.from_line("same")
    second = Message.from_line("same")
    assert first is not second
    first.text = "changed"
    assert second.text == "same"
