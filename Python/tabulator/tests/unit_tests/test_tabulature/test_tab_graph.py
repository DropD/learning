import pytest

from tabulator.notes import note_graph
from tabulator.tabulature import tab_graph


@pytest.fixture
def visitor() -> tab_graph.NotesToFretted:
    return tab_graph.NotesToFretted()


def test_visit_start(visitor):
    res = next(visitor.visit(note_graph.Node(value=note_graph.Start())))

    assert isinstance(res, tab_graph.StartNode)
