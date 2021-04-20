from collections import deque


class _A:
    pass


def exceptions() -> list[Exception]:
    return [Exception(), ValueError(), TypeError(), KeyError(), IndexError()]


def primitives() -> list[object]:
    return [None, True, False, -1, 0, 1, -1., 0., 1., 'a', 'z', '@']


def collections() -> list[object]:
    return [list(), dict(), set(), frozenset(), deque()]


def values() -> list[object]:
    return primitives() + collections() + exceptions()
