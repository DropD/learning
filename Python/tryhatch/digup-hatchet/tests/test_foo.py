from __future__ import annotations

import dataclasses

import pytest

import digup_hatchet as duha


@dataclasses.dataclass
class FooCase:
    name: str
    args: tuple[str, int, *tuple[str, ...]]
    result: str


@pytest.mark.parametrize(
    "foo_case",
    [
        FooCase("single_string", ("bar",), 'You gave me "bar".'),
        FooCase("string_int", ("bar", 42), 'You gave me "bar", "42".'),
        FooCase(
            "extra_strs",
            ("bar", 42, "extra", "strings"),
            'You gave me "bar", "42", "extra", "strings".',
        ),
    ],
    ids=lambda case: case.name,
)
def test_foo(foo_case):
    assert foo_case.result == duha.foo(*foo_case.args)
