"""
:class:`Result` forms the root type of an ADT. Values of type :class:`Result` are either instances
of :class:`Ok` or :class:`Err`. Typically this class is used to encapsulate the outcome of
evaluating an expression that may fail with an error. If evaluation succeeds, the result of the
expression is contained within an :class:`Ok`. If it fails, the error that occurred is contained
within an :class:`Err`.

Example usage::

    >>> class ParserError(ValueError): pass
    ...
    >>> def to_int(x: str) -> Result[int, ParserError]:
    ...     try:
    ...         return Ok(int(x))
    ...     except ValueError as e:
    ...         return Err(ParserError(x))
    ...
    >>> def inverse(i: int) -> Result[float, ZeroDivisionError]:
    ...     return Ok(1./i) if i != 0 else Err(ZeroDivisionError())
    ...
    >>> results = [to_int(char_).flat_map(inverse) for char_ in "1508�"]
    >>> [res.ok().unwrap() for res in results if res.is_ok]
    [1.0, 0.2, 0.125]
    >>> [res.err().unwrap() for res in results if not res.is_ok]
    [ZeroDivisionError(), ParserError('�')]

Note :class:`Result` doesn't define an analogue to the ``unwrap`` method on :class:`Maybe`. Users
must instead call e.g. `Ok(1).ok().unwrap()`. This is to limit imperative functionality to
:class:`Maybe`.
"""
from __future__ import annotations
from abc import abstractmethod, ABC
from collections.abc import Callable
from typing import Generic, NoReturn, TypeVar
from typing_extensions import final

from allusions.maybe import Maybe, Some, Empty
from allusions.types import T_co, U

E = TypeVar('E', bound=Exception)
E_co = TypeVar('E_co', covariant=True, bound=Exception)


class Result(ABC, Generic[T_co, E_co]):
    """
    A container for either the result of evaluating an expression, or the error that occurred during
    evaluation.
    """

    @property
    @abstractmethod
    def is_ok(self) -> bool:
        """
        :return: `True` if this instance represents a successfully computed value, else `False`.
        """

    @abstractmethod
    def ok(self) -> Maybe[T_co]:
        """
        :return: A :class:`Some` containing the value, if it exists, else an :class:`Empty`.
        """

    @abstractmethod
    def err(self) -> Maybe[E_co]:
        """
        :return: A :class:`Some` containing the error, if it exists, else an :class:`Empty`.
        """

    @abstractmethod
    def map_ok(self, fn: Callable[[T_co], U]) -> Result[U, E_co]:
        """
        :param fn: The function to apply to a value contained in this instance.
        :return: If this instance contains a value, a new :class:`Result` whose contained value is the result of
            applying ``fn`` to the value contained in this instance.
        """

    @abstractmethod
    def map_err(self, fn: Callable[[E_co], E]) -> Result[T_co, E]:
        """
        :param fn: The function to apply to an err contained in this instance.
        :return: If this instance contains an error, a new :class:`Result` whose contained error is
            the result of applying ``fn`` to the error contained in this instance.
        """

    @abstractmethod
    # Exception type hints here should both be F, a supertype of E_co, but that's not possible in
    # mypy, so we have to drop type safety and use Exception
    def flat_map(self, fn: Callable[[T_co], Result[U, Exception]]) -> Result[U, Exception]:
        """"""

    @abstractmethod
    def match(self, if_ok: Callable[[T_co], U], if_err: Callable[[E_co], U]) -> U:
        """
        Uses dynamic dispatch to mimic rudimentary pattern matching on this instance. If the
        instance on which this is called contains a successfully computed value, call ``if_ok`` on
        that value, and return its result. Else, call ``if_err`` on the error and return its result.

        :param if_ok: The function to call on the successfully computed value, if it exists.
        :param if_err: The function to call on the error, if it exists.
        :return: The return value of whichever of ``if_ok`` and ``if_err`` were executed.
        """


@final
class Ok(Result[T_co, NoReturn], Generic[T_co]):
    is_ok = True

    def __init__(self, o: T_co):
        """
        :param o: The value to contain.
        """
        self._o = o

    def ok(self) -> Some[T_co]:
        """
        :return: The contained value, wrapped in a :class:`Some`.
        """
        return Some(self._o)

    def err(self) -> Empty:
        """
        :return: An :class:`Empty`.
        """
        return Empty()

    def map_ok(self, fn: Callable[[T_co], U]) -> Ok[U]:
        """
        :param fn: The function to apply to the computed value.
        :return: The result of calling ``fn`` on the computed value.
        """
        return Ok(fn(self._o))

    def map_err(self, fn: object) -> Ok[T_co]:
        """
        :param fn: Unused.
        :return: The instance this method was called on, unaltered.
        """
        return self

    def flat_map(self, fn: Callable[[T_co], Result[U, E]]) -> Result[U, E]:
        return fn(self._o)

    def match(self, if_ok: Callable[[T_co], U], if_err: Callable[[E_co], U]) -> U:
        """
        :param if_ok: The function to call on the contained value.
        :param if_err: Unused.
        :return: The result of calling ``if_ok`` on the value.
        """
        return if_ok(self._o)

    def __eq__(self, other: object) -> bool:
        if type(other) == Ok:
            return self._o == other.ok().unwrap()

        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._o)

    def __repr__(self) -> str:
        return f"Ok({self._o!r})"


@final
class Err(Result[NoReturn, E_co]):
    is_ok = False

    def __init__(self, e: E_co):
        """
        :param e: The error to contain.
        """
        self._e = e

    def ok(self) -> Empty:
        """
        :return: An :class:`Empty`.
        """
        return Empty()

    def err(self) -> Some[E_co]:
        """
        :return: The contained error, wrapped in a :class:`Some`.
        """
        return Some(self._e)

    def map_ok(self, fn: Callable[[NoReturn], object]) -> Err[E_co]:
        """
        :param fn: Unused.
        :return: The instance this method was called on, unaltered.
        """
        return self

    def map_err(self, fn: Callable[[E_co], E]) -> Err[E]:
        """
        :param fn: The function to apply to the error.
        :return: The result of applying ``fn`` the error.
        """
        return Err(fn(self._e))

    def flat_map(self, fn: Callable[[NoReturn], Result[U, E]]) -> Result[U, E_co]:
        return self

    def match(self, if_ok: Callable[[NoReturn], U], if_err: Callable[[E_co], U]) -> U:
        """
        :param if_ok: Unused.
        :param if_err: The function to call on the error.
        :return: The result of calling ``if_err`` on the error.
        """
        return if_err(self._e)

    def __eq__(self, other: object) -> bool:
        if type(other) == Err:
            return self._e == other.err().unwrap()

        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._e)

    def __repr__(self) -> str:
        return f"Err({self._e!r})"
