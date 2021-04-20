from collections.abc import Callable, Hashable
from typing import TypeVar

import pytest

from allusions import Some, Empty, Maybe
from t.util import PRIMITIVES, VALUES


_T = TypeVar("_T")
_U = TypeVar("_U")


@pytest.mark.parametrize('v', PRIMITIVES)
def test_some__unwrap_returns_original_object(v: object) -> None:
    assert Some(v).unwrap() is v


def test_empty__unwrap_raises_error() -> None:
    with pytest.raises(ValueError):
        Empty().unwrap()


def _map_test_cases() -> list[tuple[_T, Callable[[_T], object]]]:
    return [
        (1, lambda x: x + 1),
        ('a', lambda s: s * 3)
        # todo more test cases
    ]


@pytest.mark.parametrize('v, fn', _map_test_cases())
def test_some__map(v: _T, fn: Callable[[_T], object]) -> None:
    assert Some(v).map(fn) == Some(fn(v))


@pytest.mark.parametrize('_, fn', _map_test_cases())
def test_empty__map(_: object, fn: Callable[[object], object]) -> None:
    assert Empty().map(fn) == Empty()


def _flat_map_test_cases() -> list[tuple[_T, Callable[[_T], Maybe[_U]], Maybe[_U]]]:
    return [
        (1, lambda x: Some(x + 1), Some(2)),
        (1, lambda x: Empty(), Empty())
        # todo more test cases
    ]


@pytest.mark.parametrize('v, fn, exp', _flat_map_test_cases())
def test_some__flat_map(v: _T, fn: Callable[[_T], Maybe[_U]], exp: Maybe[_U]) -> None:
    assert Some(v).flat_map(fn) == exp


@pytest.mark.parametrize('_v, fn, _exp', _flat_map_test_cases())
def test_empty__flat_map(_v: object, fn: Callable[[object], Maybe[_U]], _exp: object) -> None:
    assert Empty().flat_map(fn) == Empty()


@pytest.mark.parametrize('value, if_some, if_empty, exp', [
    (1, lambda x: x + 1, lambda: 0, 2),
    (1, lambda x: 'cat', lambda: 'dog', 'cat')
    # todo more test cases
])
def test_some__match(
    value: _T, if_some: Callable[[_T], _U], if_empty: Callable[[], _U], exp: _U
) -> None:
    assert Some(value).match(if_some=if_some, if_empty=if_empty) == exp


@pytest.mark.parametrize('if_some, if_empty, exp', [
    (lambda x: x + 1, lambda: 0, 0),
    (lambda x: 'cat', lambda: 'dog', 'dog')
    # todo more test cases
])
def test_empty__match(if_some: Callable[[object], _U], if_empty: Callable[[], _U], exp: _U) -> None:
    assert Empty().match(if_some=if_some, if_empty=if_empty) == exp


@pytest.mark.parametrize('v', PRIMITIVES)
def test_some__eq_is_reflexive(v: object) -> None:
    some = Some(v)
    assert some == some


@pytest.mark.parametrize('first', PRIMITIVES)
@pytest.mark.parametrize('second', PRIMITIVES)
def test_some__eq_is_symmetric(first: object, second: object) -> None:
    assert (Some(first) == Some(second)) == (Some(second) == Some(first))


def test_empty__eq_is_reflexive_and_symmetric() -> None:
    assert Empty() == Empty()


@pytest.mark.parametrize('first', PRIMITIVES)
@pytest.mark.parametrize('second', PRIMITIVES)
def test_some__neq_is_symmetric(first: object, second: object) -> None:
    assert (Some(first) != Some(second)) == (Some(second) != Some(first))


@pytest.mark.parametrize('v', VALUES)
def test_some_and_empty_are_not_equal(v: object) -> None:
    assert Some(v) != Empty() and Empty() != Some(v)


# todo test eq and neq are transitive


@pytest.mark.parametrize('hashable', PRIMITIVES + (frozenset(),))
def test_some__is_hashable_if_contents_are_hashable(hashable: Hashable) -> None:
    {Some(hashable)}


def test_empty_is_hashable() -> None:
    {Empty()}


@pytest.mark.parametrize('unhashable', [list(), dict(), set()])
def test_some__is_not_hashable_if_contents_are_not_hashable(unhashable: object) -> None:
    some = Some(unhashable)
    with pytest.raises(TypeError, match='unhashable'):
        {some}


@pytest.mark.parametrize('maybe, exp', [
    (Some(1), 'Some(1)'),
    (Some('a'), "Some('a')"),
    (Some(1.), 'Some(1.0)'),
    (Empty(), 'Empty()'),
    (Some(Some(1)), 'Some(Some(1))'),
    (Some(Some('a')), "Some(Some('a'))"),
    (Some(Empty()), 'Some(Empty())'),
])
def test_maybe__repr(maybe: Maybe[object], exp: str) -> None:
    assert repr(maybe) == exp
