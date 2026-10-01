from __future__ import annotations

from dataclasses import dataclass
from typing import final


@final
@dataclass(frozen=True)
class TextFragment:
    text: str

    def __len__(self) -> int:
        return len(self.text)

    def __mul__(self, copies: int) -> TextFragment:
        return TextFragment(self.text * copies)


@final
@dataclass(frozen=True)
class BeatFragment:
    beats: tuple[str, ...]

    def __len__(self) -> int:
        return len(self.beats)

    def __mul__(self, copies: int) -> BeatFragment:
        return BeatFragment(self.beats * copies)
