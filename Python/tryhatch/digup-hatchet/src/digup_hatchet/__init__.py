# SPDX-FileCopyrightText: 2024-present DropD <rico.haeuselmann@gmail.com>
#
# SPDX-License-Identifier: MIT
from __future__ import annotations


def foo(*args: *tuple[str, int, *tuple[str, ...]]) -> str:
    return f"You gave me {", ".join([f'"{arg}"' for arg in args])}."
