import copy
import dataclasses
import enum
import functools
import itertools
import typing
import uuid
from collections.abc import Iterator

import click

from tabulator.notes import note, note_graph, pitch


class Finger(enum.Enum):
    LeftThumb = enum.auto()
    LeftIndex = enum.auto()
    LeftMiddle = enum.auto()
    LeftRing = enum.auto()
    LeftLittle = enum.auto()
    RightThumb = enum.auto()
    RightIndex = enum.auto()
    RightMiddle = enum.auto()
    RightRing = enum.auto()
    RightLittle = enum.auto()


class Style(enum.Enum):
    UpPick = enum.auto()
    DownPick = enum.auto()
    Slide = enum.auto()
    HammerOn = enum.auto()
    PullOff = enum.auto()


@dataclasses.dataclass
class Node:
    id: uuid.UUID = dataclasses.field(init=False, default_factory=uuid.uuid1)


@dataclasses.dataclass
class Edge:
    id: uuid.UUID = dataclasses.field(init=False, default_factory=uuid.uuid1)
    src: Node
    tgt: Node
    difficulty: int | None = None
    interest: int | None = None


@dataclasses.dataclass
class MiddleNode(Node):
    next: list[Edge]
    prev: list[Edge]


@dataclasses.dataclass
class StartNode(Node):
    """Tab tree root node."""

    next: list[Edge]


@dataclasses.dataclass
class EndNode(Node):
    prev: list[Edge]


@dataclasses.dataclass
class RestNode(MiddleNode): ...


@dataclasses.dataclass
class FrettedNode(MiddleNode):
    string: int
    fret: int


@dataclasses.dataclass
class FingeredNode(FrettedNode):
    finger: Finger


@dataclasses.dataclass
class StyledNode(FingeredNode):
    style: Style


@dataclasses.dataclass
class NotesToFretted:
    strings: tuple[pitch.Pitch, ...] = (
        pitch.Pitch.from_base_semi_octave("e", 0, 4),
        pitch.Pitch.from_base_semi_octave("b", 0, 3),
        pitch.Pitch.from_base_semi_octave("g", 0, 3),
        pitch.Pitch.from_base_semi_octave("d", 0, 3),
        pitch.Pitch.from_base_semi_octave("a", 0, 2),
        pitch.Pitch.from_base_semi_octave("b", 0, 1),
    )
    max_frets: int = 24

    @functools.singledispatchmethod
    def visit(self, node: note_graph.Node) -> Iterator[Node]:
        new_nodes = list(self.visit(node.value))
        next_nodes = list(self.visit(node.next))
        for new, next_node in itertools.product(new_nodes, next_nodes):
            edge = Edge(src=new, tgt=next_node, difficulty=None)
            match new:
                case StartNode() | MiddleNode():
                    new.next.append(edge)
                case _:
                    pass

            match next:
                case EndNode() | MiddleNode():
                    next.prev.append(edge)
                case _:
                    pass

        yield from new_nodes

    @visit.register
    def visit_none(self, node: None) -> Iterator[Node]:  # noqa ARG002
        yield from []

    @visit.register
    def visit_start(self, node: note_graph.Start) -> Iterator[StartNode]:  # noqa ARG002
        yield StartNode(next=[])

    @visit.register
    def visit_end(self, node: note_graph.End) -> Iterator[EndNode]:  # noqa ARG002
        yield EndNode(prev=[])

    @visit.register
    def visit_note(self, node: note.Note) -> Iterator[FrettedNode]:
        for string_index, string in enumerate(self.strings):
            if node.pitch.value in range(string.value, string.value + self.max_frets):
                yield FrettedNode(
                    string=string_index,
                    fret=(node.pitch - string).value,
                    next=[],
                    prev=[],
                )

    @visit.register
    def visit_rest(self, node: note.Rest) -> Iterator[RestNode]:  # noqa ARG002
        yield RestNode(next=[], prev=[])


def build_from_notes(notes: note_graph.Node) -> StartNode:
    if not isinstance(notes.value, note_graph.Start):
        msg = (
            "Parameter 'notes' must be a start node."
            "\n Hint: Use NotesToFretted directly to build "
            "tab graph from fragments."
        )
        raise TypeError(msg)
    return typing.cast(StartNode, next(NotesToFretted().visit(notes)))


@dataclasses.dataclass
class TxtTab:
    n_strings: int = 6

    @functools.singledispatchmethod
    def visit(
        self,
        node: Node,  # noqa ARG002
        *,
        sequence: list[list[str]],
    ) -> Iterator[list[list[str]]]:
        yield sequence

    @visit.register
    def visit_start(self, node: StartNode | MiddleNode, *, sequence: list[list[str]]) -> Iterator[list[list[str]]]:
        for edge in node.next:
            yield from self.visit(edge.tgt, sequence=copy.copy(sequence))

    @visit.register
    def visit_fretted(self, node: FrettedNode, *, sequence: list[list[str]]) -> Iterator[list[list[str]]]:
        lines = ["---"] * self.n_strings
        lines[node.string] = f"{node.fret:^3}"
        sequence.append(lines)
        for edge in node.next:
            yield from self.visit(edge.tgt, sequence=copy.copy(sequence))

    @visit.register
    def visit_rest(self, node: RestNode, *, sequence: list[list[str]]) -> Iterator[list[list[str]]]:
        sequence.append(["---"] * self.n_strings)
        for edge in node.next:
            yield from self.visit(edge.tgt, sequence=copy.copy(sequence))


def txt_tab_echo_all(tree: StartNode, *, tabber: TxtTab | None = None) -> None:
    tabber = tabber or TxtTab()
    for sequence in tabber.visit(tree, sequence=[]):
        click.echo("")
        for i in range(tabber.n_strings):
            click.echo("".join([pos[i] for pos in sequence]))
            click.echo("".join([pos[i] for pos in sequence]))
