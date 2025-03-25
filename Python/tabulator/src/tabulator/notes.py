import dataclasses
from typing import Self


NOTENAME_TO_VALUE: dict[str, int] = {
    "c": 0,
    "d": 2,
    "e": 4,
    "f": 5,
    "g": 7,
    "a": 9,
    "b": 11,
}

VALUE_TO_NOTE = ["c", "cis", "d", "dis", "e", "f", "fis", "g", "gis", "a", "bes", "b"]


@dataclasses.dataclass
class Pitch:
    value: int

    @classmethod
    def from_base_semi_octave(cls, basenote: str, semi: int, octave: int) -> Self:
        return cls(12 * octave + NOTENAME_TO_VALUE[basenote.lower()] + semi)

    def __str__(self) -> str:
        octave = self.value // 12 - 3
        note_name = VALUE_TO_NOTE[self.value % 12]
        octave_str = ""
        if octave > 0:
            octave_str = "'" * octave
        elif octave < 0:
            octave_str = "," * (-octave)
        return f"{note_name}{octave_str}"
