from __future__ import annotations

import dataclasses
import re
import typing
from typing import Self

from tabulator import exceptions
from tabulator.notes import note, pitch

if typing.TYPE_CHECKING:
    import pathlib
    from collections.abc import Iterator


@dataclasses.dataclass
class Fragment:
    sequence: list[note.Note | note.Rest]


@dataclasses.dataclass
class Token:
    value: str
    lineno: int
    end_lineno: int
    offset: int
    end_offset: int
    filename: str

    @classmethod
    def from_str(cls, value: str) -> Self:
        return cls(
            value=value,
            lineno=1,
            end_lineno=2,
            offset=1,
            end_offset=len(value),
            filename="<string>",
        )


def build_from_file(path: pathlib.Path) -> Fragment:
    return Fragment([note_from_token(token) for token in tokenize(path.read_text(), filename=str(path.absolute()))])


def tokenize(fragment_str: str, *, filename: str | None = None) -> Iterator[Token]:
    lines = fragment_str.splitlines()
    for lineno, line in enumerate(lines):
        rest = line
        offset = 0
        while rest:
            next_whitespace = re.search(r"\s", rest)
            token_value = rest
            offset_end = offset + len(rest)
            next_start = len(rest)
            if next_whitespace:
                token_value = rest[: next_whitespace.start()]
                offset_end = next_whitespace.start() + offset
                next_start = next_whitespace.end()
            rest = rest[next_start:]
            if token_value:
                yield Token(
                    value=token_value,
                    lineno=lineno + 1,
                    end_lineno=lineno + 2,
                    offset=offset,
                    end_offset=offset_end,
                    filename=filename or "<string>",
                )
            offset += next_start


def build_from_string(fragment_str: str) -> Fragment:
    return Fragment([note_from_token(token) for token in tokenize(fragment_str)])


def note_from_token(token: Token) -> note.Note | note.Rest:
    parsed = re.match(
        r"^(?P<basevalue>[abcdefgr])(?P<semistep>(is)|(es)|(s))?(?P<octave>('*)(,*))?(?P<duration>\d*)$",
        token.value,
    )
    if parsed is None:
        raise exceptions.NoteParsingError.from_token(token)
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
            msg = "Only \"'\" or '\"' are allowed as octave indicators."
            raise ValueError(msg)
    if groups["basevalue"] == "r":
        return note.Rest(duration=int(groups["duration"]))
    return note.Note(
        pitch=pitch.Pitch.from_base_semi_octave(basenote=groups["basevalue"], semi=semistep, octave=octave),
        duration=int(groups["duration"]),  # seconds for hardcoded tempo 120 # TODO: allow other tempi
    )
