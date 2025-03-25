import dataclasses
import enum
import functools
import itertools
import uuid
from typing import Iterator, Optional

from tabulator import notes, note_graph, note_fragment


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
    id: uuid.UUID = dataclasses.field(init=False, default_factory=uuid.uuid1())


@dataclasses.dataclass
class Edge:
    id: uuid.UUID = dataclasses.field(init=False, default_factory=uuid.uuid1())
    src: Node
    tgt: Node
    difficulty: Optional[int] = None
    interest: Optional[int] = None


@dataclasses.dataclass
class MiddleNode:
    next: list[Edge]
    prev: list[Edge]


@dataclasses.dataclass
class StartNode(Node):
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
    strings: tuple[notes.Pitch] = (
        notes.Pitch.from_base_semi_octave("e", 0, 4),
        notes.Pitch.from_base_semi_octave("h", 0, 3),
        notes.Pitch.from_base_semi_octave("g", 0, 3),
        notes.Pitch.from_base_semi_octave("d", 0, 3),
        notes.Pitch.from_base_semi_octave("a", 0, 2),
        notes.Pitch.from_base_semi_octave("h", 0, 1),
    )
    max_frets: int = 24

    @functools.singledispatchmethod
    def visit(self, node: note_graph.Node) -> Iterator[Node]:
        new_nodes = self.visit(node.value)
        next_nodes = self.visit(node.next)
        for new, next in itertools.product(new_nodes, next_nodes):
            edge = Edge(src=new, tgt=next, difficulty=None)
            new.next.append(edge)
            next.prev.append(edge)

        yield from new_nodes

    @visit.register
    def visit(self, node: None) -> Iterator[Node]:
        yield from []

    @visit.register
    def visit_start(self, node: note_graph.Start) -> Iterator[Node]:
        yield StartNode(next=[])

    @visit.register
    def visit_end(self, node: note_graph.End) -> Iterator[Node]:
        yield EndNode(prev=[])

    @visit.register
    def visit_note(self, node: note_fragment.Note) -> Iterator[Node]:
        for string in self.strings:
            if node.pitch.value in range(string, string + self.max_frets):
                yield FrettedNode(string=string, fret=node.pitch.value - string, next=[], prev=[])

    @visit.register
    def visit_rest(self, node: note_fragment.Rest) -> Iterator[Node]:
        yield RestNode(next=[], prev=[])
