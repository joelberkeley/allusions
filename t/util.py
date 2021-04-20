from __future__ import annotations
from collections import deque
from typing import Final


class _A:
    pass


# todo list, set and dict are primitives, no? but they're also collections, so how to sort?
PRIMITIVES: Final[tuple[object, ...]] = (None, True, False, -1, 0, 1, -1., 0., 1., 'a', 'z', '@')

COLLECTIONS: Final[tuple[object, ...]] = (
    tuple(),
    (1, ('a', (True,))),
    list(),
    [1, ['a', [True]]],
    dict(),
    {1: {'a': {True: None}}},
    set(),
    {1, {'a', {True}}},
    frozenset(),
    frozenset({1, {'a', {True}}}),
    deque(),
    deque([1, ['a', [True]]]),
)

EXCEPTIONS: Final[tuple[Exception, ...]] = (Exception(), ValueError(), TypeError(), KeyError())

VALUES: Final[tuple[object, ...]] = PRIMITIVES + EXCEPTIONS + COLLECTIONS + (_A(),)
