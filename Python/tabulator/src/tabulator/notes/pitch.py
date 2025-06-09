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
        octave = self.octave
        note_name = self.note
        octave_str = ""
        if octave > 0:
            octave_str = "'" * octave
        elif octave < 0:
            octave_str = "," * (-octave)
        return f"{note_name}{octave_str}"

    @property
    def octave(self):
        return self.value // 12 - 3

    @property
    def note(self):
        return VALUE_TO_NOTE[self.value % 12]

    def __sub__(self, other: Self) -> Self:
        return self.__class__(self.value - other.value)
        return self.__class__(self.value - other.value)
