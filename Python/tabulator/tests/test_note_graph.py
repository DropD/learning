import pytest

from tabulator import note_graph, note_fragment


@pytest.fixture
def fragment():
    snippet = "b,,16 r16 b,,8 fis16 fis,16 f,16 e,16"
    return note_fragment.build_from_string(snippet)


def test_build_from_fragment(fragment):
    testee = note_graph.build_from_fragment(fragment)
    assert isinstance(testee.value, note_graph.Start)
    last = list(iter(testee))[-1]
    assert isinstance(last.value, note_graph.End)
