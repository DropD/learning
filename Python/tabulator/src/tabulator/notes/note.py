from __future__ import annotations

import dataclasses
import typing

if typing.TYPE_CHECKING:
    from tabulator.notes import pitch


@dataclasses.dataclass
class Note:
    pitch: pitch.Pitch
    duration: int

    def __str__(self) -> str:
        return f"{self.pitch}{self.duration}"


@dataclasses.dataclass
class Rest:
    duration: int

    def __str__(self) -> str:
        return f"r{self.duration}"
