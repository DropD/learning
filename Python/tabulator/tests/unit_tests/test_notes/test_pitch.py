import pytest

from tabulator.notes import pitch


@pytest.mark.parametrize("case", [("c", 0, 0, 0), ("d", 1, 1, 15), ("b", -1, 4, 58)])
def test_pitch_from_base_semi_octave(case):
    base, semi, octave, ref = case
    assert pitch.Pitch.from_base_semi_octave(basenote=base, semi=semi, octave=octave).value == ref


@pytest.mark.parametrize("case", [(0, "c,,,"), (15, "dis,,"), (58, "bes'")])
def test_pitch_str(case):
    value, ref = case
    assert str(pitch.Pitch(value=value)) == ref
