import dataclasses
import pathlib
import re

from tabulator import notes


@dataclasses.dataclass
class Note:
    pitch: notes.Pitch
    duration: int

    def __str__(self) -> str:
        return f"{self.pitch}{self.duration}"


@dataclasses.dataclass
class Rest:
    duration: int

    def __str__(self) -> str:
        return f"r{self.duration}"


@dataclasses.dataclass
class Fragment:
    sequence: list[Note | Rest]


def build_from_file(path: pathlib.Path) -> Fragment:
    return build_from_string(path.read_text())


def build_from_string(fragment_str: str) -> Fragment:
    fragment = Fragment([])
    for token in fragment_str.split(" "):
        fragment.sequence.append(note_from_token(token))
    return fragment


def note_from_token(token: str) -> Note:
    parsed = re.match(
        r"^(?P<basevalue>[abcdefgr])(?P<semistep>(is)|(es)|(s))?(?P<octave>('*)(,*))?(?P<duration>\d*)$",
        token,
    )
    groups = parsed.groupdict()
    semistep = 0
    if parsed_semi := groups["semistep"]:
        semistep = 1 if parsed_semi == "is" else -1
    octave = 3
    if parsed_oct := groups["octave"]:
        if (chars := set(parsed_oct)) == {"'"}:
            octave += len(parsed_oct)
        elif chars == {","}:
            octave -= len(parsed_oct)
        else:
            raise ValueError("Only \"'\" and '\"' are allowed as octave indicators.")
    if groups["basevalue"] == "r":
        return Rest(duration=int(groups["duration"]))
    return Note(
        pitch=notes.Pitch.from_base_semi_octave(
            basenote=groups["basevalue"], semi=semistep, octave=octave
        ),
        duration=int(
            groups["duration"]
        ),  # seconds for hardcoded tempo 120 # TODO: allow other tempi
    )
