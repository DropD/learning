from tabulator import tab_graph, note_graph

import pytest


@pytest.fixture
def visitor() -> tab_graph.NotesToFretted:
    return tab_graph.NotesToFretted()


def test_visit_start(visitor):
    res = next(visitor.visit(note_graph.Node(value=note_graph.Start())))

    assert isinstance(res, tab_graph.StartNode)
