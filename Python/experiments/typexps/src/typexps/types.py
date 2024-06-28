from __future__ import annotations
import dataclasses
import typing
from typing import Any
from typing_extensions import Self


A = typing.TypeVar("A")
A_contra = typing.TypeVar("A_contra", contravariant=True)
B = typing.TypeVar("B")
B_co = typing.TypeVar("B_co", covariant=True)
C = typing.TypeVar("C")


def compose(f: Func[B, C], g: Func[A, B]) -> Compose[A, C]:
    @dataclasses.dataclass(frozen=True)
    class Composition(Compose[A, C]):

        __name__ = f"{f.__name__} . {g.__name__}"

        def __call__(self, x: A) -> C:
            return f(g(x))

    return Composition()


class Func(typing.Protocol[A_contra, B_co]):

    def __call__(self, x: A_contra) -> B_co:
        ...

    @property
    def __name__(self) -> str:
        ...


class Plus(typing.Protocol):

    def __add__(self, other: Self) -> Self:
        ...


@dataclasses.dataclass(frozen=True, init=False)
class Compose(Func[A, B]):

    def compose(self, other: Func[C, A]) -> Compose[C, B]:
        return compose(self, other)

    def __rshift__(self, other: Compose[B, C]) -> Compose[A, C]:
        return other.compose(self)


@dataclasses.dataclass(frozen=True, init=False)
class Replace(typing.Protocol):

    def replace(self, **kwargs: Any) -> Self:
        if not dataclasses.is_dataclass(self.__class__):
            raise TypeError(f"{self.__class__} is no dataclass!")
        return dataclasses.replace(self, **kwargs)


ReplaceT = typing.TypeVar("ReplaceT", bound=Replace)
FuncT = typing.TypeVar("FuncT", bound=Func)
PlusT = typing.TypeVar("PlusT", bound=Plus)


@dataclasses.dataclass(frozen=True)
class AddN(Replace, Compose[PlusT, PlusT]):
    n: PlusT

    def __call__(self, x: PlusT) -> PlusT:
        return x + self.n

    @property
    def __name__(self) -> str:
        return f"(+{self.n})"

    @typing.overload
    def compose(self, other: Self) -> Self:
        ...

    @typing.overload
    def compose(self, other: Func[C, PlusT]) -> Compose[C, PlusT]:
        ...

    def compose(self, other: Func[C, PlusT]) -> Compose[C, PlusT]:
        match other:
            case AddN(n=other_n):
                return AddN(n=other_n + self.n)
            case _:
                return compose(self, other)

    @typing.overload
    def __rshift__(self, other: Self) -> Self:
        ...

    @typing.overload
    def __rshift__(self, other: Compose[PlusT, C]) -> Compose[PlusT, C]:
        ...

    def __rshift__(self, other: Compose[PlusT, C]) -> Compose[PlusT, C]:
        return super().__rshift__(other)


def test_replace_typing(f: AddN) -> None:
    ...


ADDER = AddN(n=1)
test_replace_typing(ADDER)
test_replace_typing(ADDER.replace(n=5))
