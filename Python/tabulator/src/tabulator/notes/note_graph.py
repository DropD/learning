import dataclasses
import functools
import itertools
import pathlib
import uuid
from collections.abc import Iterator
from typing import Any, Self

from tabulator.notes import note, note_sequence


@dataclasses.dataclass
class Start:
    id: uuid.UUID = dataclasses.field(init=False, default_factory=uuid.uuid1)


@dataclasses.dataclass
class End:
    id: uuid.UUID = dataclasses.field(init=False, default_factory=uuid.uuid1)


@dataclasses.dataclass
class Node:
    id: uuid.UUID = dataclasses.field(init=False, default_factory=uuid.uuid1)
    value: note.Note | note.Rest | Start | End
    next: Self | None = None

    def __iter__(self) -> Iterator[Self]:
        current: Self | None = self
        while current:
            yield current
            current = current.next


@dataclasses.dataclass
class Builder:
    @functools.singledispatchmethod
    def visit(self, obj: Any) -> Node:
        raise NotImplementedError

    @visit.register
    def visit_fragment(self, obj: note_sequence.Fragment) -> Node:
        nodes = [Node(value=Start())] + [self.visit_note(note) for note in obj.sequence] + [Node(value=End())]
        for cur, following in itertools.pairwise(nodes):
            cur.next = following
        return nodes[0]

    @visit.register
    def visit_note(self, obj: note.Note | note.Rest) -> Node:
        return Node(value=obj)


def build_from_fragment(fragment: note_sequence.Fragment) -> Node:
    return Builder().visit(fragment)


def build_from_string(fragment_str: str) -> Node:
    return build_from_fragment(note_sequence.build_from_string(fragment_str))


def build_from_file(path: pathlib.Path) -> Node:
    return build_from_fragment(note_sequence.build_from_file(path))
