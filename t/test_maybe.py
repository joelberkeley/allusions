from collections.abc import Callable
from typing import TypeVar

import pytest

from allusions import Some, Empty, Maybe
from t.util import primitives, values


_T = TypeVar("_T")
_U = TypeVar("_U")


@pytest.mark.parametrize('v', primitives())
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
def test_empty__map(_, fn: Callable[[object], object]) -> None:
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


@pytest.mark.parametrize('_, fn, exp', _flat_map_test_cases())
def test_empty__flat_map(_: object, fn: Callable[[object], Maybe[_U]], exp: Maybe[_U]) -> None:
    assert Empty().flat_map(fn) == Empty()


@pytest.mark.parametrize('value, if_some, if_empty, exp', [
    (1, lambda x: x + 1, lambda: 0, 2),
    (1, lambda x: 'cat', lambda: 'dog', 'cat')
    # todo more test cases
])
def test_some__match(value, if_some, if_empty, exp) -> None:
    assert Some(value).match(if_some=if_some, if_empty=if_empty) == exp


@pytest.mark.parametrize('if_some, if_empty, exp', [
    (lambda x: x + 1, lambda: 0, 0),
    (lambda x: 'cat', lambda: 'dog', 'dog')
    # todo more test cases
])
def test_empty__match(if_some, if_empty, exp) -> None:
    assert Empty().match(if_some=if_some, if_empty=if_empty) == exp


@pytest.mark.parametrize('v', primitives())
def test_some__eq_is_reflexive(v: object) -> None:
    some = Some(v)
    assert some == some


# todo shouldn't we be testing lhs is the same as rhs, not that they're both equal?
@pytest.mark.parametrize('first, second', [(v, v) for v in primitives()])
def test_some__eq_is_symmetric(first: _T, second: _T) -> None:
    assert Some(first) == Some(second) and Some(second) == Some(first)


def test_empty__eq_is_reflexive_and_symmetric() -> None:
    assert Empty() == Empty()


@pytest.mark.parametrize('first', primitives())
@pytest.mark.parametrize('second', primitives())
def test_some__neq_is_symmetric(first, second) -> None:
    if first != second:
        assert Some(first) != Some(second) and Some(second) != Some(first)


@pytest.mark.parametrize('v', values())
def test_some_and_empty_are_not_equal(v) -> None:
    assert Some(v) != Empty() and Empty() != Some(v)


# todo test eq and neq are transitive


@pytest.mark.parametrize('hashable', primitives() + [frozenset()])
def test_some__is_hashable_if_contents_are_hashable(hashable) -> None:
    {Some(hashable)}


def test_empty_is_hashable() -> None:
    {Empty()}


@pytest.mark.parametrize('unhashable', [list(), dict(), set()])
def test_some__is_not_hashable_if_contents_are_not_hashable(unhashable) -> None:
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
def test_maybe__repr(maybe, exp) -> None:
    assert repr(maybe) == exp
