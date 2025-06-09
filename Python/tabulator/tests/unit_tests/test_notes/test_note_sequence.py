import pytest

from tabulator import exceptions
from tabulator.notes import note, note_sequence, pitch


@pytest.mark.parametrize(
    "case",
    [
        ("a4", note.Note(pitch=pitch.Pitch(45), duration=4)),
        ("b''8", note.Note(pitch=pitch.Pitch(71), duration=8)),
        ("ces,1", note.Note(pitch=pitch.Pitch(23), duration=1)),
        ("gis16", note.Note(pitch=pitch.Pitch(44), duration=16)),
    ],
    ids=lambda x: x[0],
)
def test_note_from_token(case):
    token, ref = case
    assert note_sequence.note_from_token(note_sequence.Token.from_str(token)) == ref


def test_note_from_token_unparseable():
    with pytest.raises(exceptions.NoteParsingError):
        note_sequence.note_from_token(note_sequence.Token.from_str("notanote"))


def test_note_from_token_invalid_note():
    with pytest.raises(exceptions.NoteParsingError):
        note_sequence.note_from_token(note_sequence.Token.from_str("i4"))


def test_note_from_token_bad_octave():
    with pytest.raises(ValueError, match="octave indicator"):
        note_sequence.note_from_token(note_sequence.Token.from_str("a',4"))


def test_build_from_string():
    testee = "b,,16 r16 b,,8 fis16 fis,16 f,16 e,16"
    fragment = note_sequence.build_from_string(testee)
    assert len(fragment.sequence) == 7
    assert " ".join(str(note) for note in fragment.sequence) == testee
