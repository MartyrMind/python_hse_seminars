import tempfile
from pathlib import Path
from typing import TextIO, cast


def make_temp(target: Path) -> tuple[Path, TextIO]:
    """Создать текстовый временный файл рядом с target и вернуть путь и поток."""
    stream = tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=target.parent,
        prefix=f".{target.name}.",
        suffix=".tmp",
        delete=False,
    )
    return Path(stream.name), cast(TextIO, stream)


class AtomicExport:
    errors: list[Exception]

    def __init__(
        self,
        target: Path,
        *,
        allowed: tuple[type[Exception], ...] = (),
        limit: int = 0,
    ) -> None:
        raise NotImplementedError("Implement me")
