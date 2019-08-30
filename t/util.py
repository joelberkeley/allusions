from typing import Any, List


class _A:
    pass


def exceptions() -> List[Exception]:
    return [Exception(), ValueError(), TypeError(), KeyError(), IndexError()]


def primitives() -> List[Any]:
    return [None, True, False, -1, 0, 1, -1., 0., 1., 'a', 'z', '@']
