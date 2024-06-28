import pytest  # noqa F401

from typexps import types

__author__ = "DropD"
__copyright__ = "DropD"
__license__ = "MIT"


def test_compose_functions() -> None:
    def f(x: tuple[int, str]) -> str:
        return f"{x[0]} == {x[1]}"

    def g(x: int) -> tuple[int, str]:
        return x, str(x)

    f_of_g: types.Func[int, str] = types.compose(f, g)
    assert f_of_g.__name__ == "f . g"

    result: str = f_of_g(5)
    assert result == "5 == 5"


def test_compose_keeps_replace() -> None:
    add_8: types.AddN[int] = types.AddN(5).compose(types.AddN(3))
    assert add_8.n == 8

    result: int = add_8(1)
    assert result == 9

    add_42: types.AddN[int] = add_8.replace(n=42)
    assert add_42.n == 42
    assert add_42(0) == 42


def test_rshift_keeps_replace() -> None:
    add_8: types.AddN[float] = types.AddN(5.0) >> types.AddN(3.0)
    assert add_8.n == 8.0

    result: float = add_8(1.0)
    assert result == 9.0

    add_42: types.AddN[float] = add_8.replace(n=42.0)
    assert add_42.n == 42.0
    assert add_42(0) == 42.0
