import pytest

from tabulator import note_fragment, notes


@pytest.mark.parametrize(
    "case",
    [
        ("a4", note_fragment.Note(pitch=notes.Pitch(45), duration=4)),
        ("b''8", note_fragment.Note(pitch=notes.Pitch(71), duration=8)),
        ("ces,1", note_fragment.Note(pitch=notes.Pitch(23), duration=1)),
        ("gis16", note_fragment.Note(pitch=notes.Pitch(44), duration=16)),
    ],
    ids=lambda x: x[0],
)
def test_note_from_token(case):
    token, ref = case
    assert note_fragment.note_from_token(token) == ref


def test_build_from_string():
    testee = "b,,16 r16 b,,8 fis16 fis,16 f,16 e,16"
    fragment = note_fragment.build_from_string(testee)
    assert len(fragment.sequence) == 7
    assert " ".join(str(note) for note in fragment.sequence) == testee
