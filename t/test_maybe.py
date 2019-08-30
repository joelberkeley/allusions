from typing import List, Any, Callable, Tuple, TypeVar

import pytest

from allusions import Some, Empty, Maybe
from t.util import primitives


@pytest.mark.parametrize('v', primitives())
def test_some__unwrap_returns_original_object(v) -> None:
    assert Some(v).unwrap() is v


def test_empty__unwrap_raises_error() -> None:
    with pytest.raises(ValueError):
        Empty().unwrap()


T = TypeVar('T')
U = TypeVar('U')


def _map_test_cases() -> List[Tuple[Any, Callable[[Any], Any]]]:
    return [
        (1, lambda x: x + 1),
        ('a', lambda s: s * 3)
        # todo more test cases
    ]


@pytest.mark.parametrize('v, fn', _map_test_cases())
def test_some__map(v, fn) -> None:
    assert Some(v).map(fn) == Some(fn(v))


@pytest.mark.parametrize('v, fn', _map_test_cases())
def test_empty__map(v, fn) -> None:
    assert Empty().map(fn) == Empty()


def _flat_map_test_cases() -> List[Tuple[Any, Callable[[Any], Maybe[Any]], Maybe[Any]]]:
    return [
        (1, lambda x: Some(x + 1), Some(2)),
        (1, lambda x: Empty(), Empty())
        # todo more test cases?
    ]


@pytest.mark.parametrize('v, fn, exp', [
    (1, lambda x: Some(x + 1), Some(2)),
    (1, lambda x: Empty(), Empty())
    # todo more test cases?
])
def test_some__flat_map(v, fn, exp) -> None:
    assert Some(v).flat_map(fn) == exp


@pytest.mark.parametrize('_, fn, exp', _flat_map_test_cases())
def test_empty__flat_map(_, fn, exp) -> None:
    assert Empty().flat_map(fn) == Empty()


def test_some__match() -> None:
    # todo more test cases
    assert Some(1).match(some=lambda x: x + 1, empty=lambda: 0) == 2


def test_empty__match() -> None:
    # todo more test cases
    assert Empty().match(some=lambda x: x + 1, empty=lambda: 0) == 0


@pytest.mark.parametrize('v', primitives())
def test_some__eq_is_reflexive(v) -> None:
    some = Some(v)
    assert some == some


@pytest.mark.parametrize('first, second', [(v, v) for v in primitives()])
def test_some__eq_is_symmetric(first, second) -> None:
    assert Some(first) == Some(second) and Some(second) == Some(first)


def test_empty__eq_is_reflexive_and_symmetric() -> None:
    assert Empty() == Empty()


# todo test neq is symmetric

# todo test transitive

@pytest.mark.parametrize('maybe, exp', [
    (Some(1), 'Some(1)'),
    (Some('a'), "Some('a')"),
    (Some(1.), 'Some(1.0)'),
    (Empty(), 'Empty()'),
])
def test_maybe__repr(maybe, exp) -> None:
    assert repr(maybe) == exp
