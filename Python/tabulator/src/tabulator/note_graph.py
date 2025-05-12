import dataclasses
import functools
import itertools
import pathlib
import uuid
from typing import Any, Optional, Self, Iterator
from tabulator import note_fragment


@dataclasses.dataclass
class Start:
    id: uuid.UUID = dataclasses.field(init=False, default_factory=uuid.uuid1)


@dataclasses.dataclass
class End:
    id: uuid.UUID = dataclasses.field(init=False, default_factory=uuid.uuid1)


@dataclasses.dataclass
class Node:
    id: uuid.UUID = dataclasses.field(init=False, default_factory=uuid.uuid1)
    value: note_fragment.Note | note_fragment.Rest | Start | End
    next: Optional[Self] = None

    def __iter__(self) -> Iterator[Self]:
        current = self
        while current:
            yield current
            current = current.next


@dataclasses.dataclass
class Builder:
    @functools.singledispatchmethod
    def visit(self, obj: Any) -> Node:
        raise NotImplementedError()

    @visit.register
    def visit_fragment(self, obj: note_fragment.Fragment) -> Node:
        nodes = (
            [Node(value=Start())]
            + [self.visit_note(note) for note in obj.sequence]
            + [Node(value=End())]
        )
        for cur, following in itertools.pairwise(nodes):
            cur.next = following
        return nodes[0]

    @visit.register
    def visit_note(self, obj: note_fragment.Note | note_fragment.Rest) -> Node:
        return Node(value=obj)


def build_from_fragment(fragment: note_fragment.Fragment) -> Node:
    return Builder().visit(fragment)


def build_from_string(fragment_str: str) -> Node:
    return build_from_fragment(note_fragment.build_from_string(fragment_str))


def build_from_file(path: pathlib.Path) -> Node:
    return build_from_fragment(note_fragment.build_from_file(path))
