from __future__ import annotations

import pathlib
import textwrap
import typing
from typing import Self

if typing.TYPE_CHECKING:
    import note_fragment


class NoteParsingError(SyntaxError):
    """Error while parsing a note sequence string."""

    def __init__(
        self,
        text: str,
        *,
        lineno: int,
        end_lineno: int,
        offset: int,
        end_offset: int,
        filename: str,
    ):
        super().__init__(text)
        self.lineno = lineno
        self.end_lineno = end_lineno
        self.offset = offset
        self.end_offset = end_offset
        self.filename = filename

    @classmethod
    def from_token(cls, token: note_fragment.Token, text: str | None = None) -> Self:
        text = (
            text or f"Error parsing note at line {token.lineno}, column {token.offset}."
        )
        lines = [text, textwrap.indent(token.value, "  ")]
        if token.filename != "<string>":
            filepath = pathlib.Path(token.filename)
            lines = (
                [text]
                + textwrap.indent(filepath.read_text(), "  ").splitlines()[
                    (token.lineno - 1) : (token.end_lineno - 1)
                ]
                + [
                    "  "
                    + " " * (token.offset - 1)
                    + "^"
                    + "~" * (token.end_offset - token.offset - 1)
                ]
            )
        return cls(
            "\n".join(lines),
            lineno=token.lineno,
            end_lineno=token.end_lineno,
            offset=token.offset,
            end_offset=token.end_offset,
            filename=token.filename,
        )

    def __str__(self) -> str:
        lines = []
        if self.filename and self.lineno:
            filepath = pathlib.Path(self.filename)
            lines = filepath.read_text().splitlines()[
                (self.lineno - 1) : ((self.end_lineno or (self.lineno + 1)) - 1)
            ]
        return "\n".join(lines + [super().__str__(self)])
