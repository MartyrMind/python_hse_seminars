class Message:
    def __init__(self, text: str) -> None:
        self.text = text

    def render(self) -> str:
        return self.text


class LoudMessage(Message):
    def render(self) -> str:
        return self.text.upper()


class QuotedMessage(Message):
    def render(self) -> str:
        return f"«{self.text}»"
