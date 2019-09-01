from collections import deque
from typing import Any, List


class _A:
    pass


def exceptions() -> List[Exception]:
    return [Exception(), ValueError(), TypeError(), KeyError(), IndexError()]


def primitives() -> List[Any]:
    return [None, True, False, -1, 0, 1, -1., 0., 1., 'a', 'z', '@']


def collections() -> List[Any]:
    return [list(), dict(), set(), frozenset(), deque()]


def values() -> List[Any]:
    return primitives() + collections() + exceptions()
