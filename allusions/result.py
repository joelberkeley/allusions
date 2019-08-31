"""
Note we don't provide an unwrap method. Users must call `Ok(1).ok().unwrap()`. This is to limit imperative functionality
to `Maybe`.
"""
from abc import abstractmethod, ABC
from typing import Generic, TypeVar, Callable, NoReturn, Any
from typing_extensions import final

from allusions.maybe import Maybe, Some, Empty

T_co = TypeVar('T_co', covariant=True)
E_co = TypeVar('E_co', covariant=True, bound=Exception)

U = TypeVar('U')
F = TypeVar('F', bound=Exception)


class Result(ABC, Generic[T_co, E_co]):
    """ A container for either the result of evaluating an expression, or the error that occurred during evaluation. """
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
    def map_ok(self, fn: Callable[[T_co], U]) -> 'Result[U, E_co]':
        """
        :param fn: The function to apply to a value contained in this instance.
        :return: If this instance contains a value, a new :class:`Result` whose contained value is the result of
            applying ``fn`` to the value contained in this instance.
        """

    @abstractmethod
    def map_err(self, fn: Callable[[E_co], F]) -> 'Result[T_co, F]':
        """
        :param fn: The function to apply to an err contained in this instance.
        :return: If this instance contains an error, a new :class:`Result` whose contained error is the result of
            applying ``fn`` to the error contained in this instance.
        """

    @abstractmethod
    def match(self, if_ok: Callable[[T_co], U], if_err: Callable[[E_co], U]) -> U:
        """
        Uses dynamic dispatch to mimic rudimentary pattern matching on this instance. If the instance on which
        this is called contains a successfully computed value, call ``if_ok`` on that value, and return its result.
        Else, call ``if_err`` on the error and return its result.

        :param if_ok: The function to call on the successfully computed value, if it exists.
        :param if_err: The function to call on the error, if it exists.
        :return: The return value of whichever of ``if_ok`` and ``if_err`` were executed.
        """


@final
class Ok(Result[T_co, NoReturn], Generic[T_co]):
    def __init__(self, o: T_co):
        """
        :param o: The value to contain.
        """
        self._o = o

    def ok(self) -> 'Some[T_co]':
        """
        :return: The contained value, wrapped in a :class:`Some`.
        """
        return Some(self._o)

    def err(self) -> Empty:
        """
        :return: An :class:`Empty`.
        """
        return Empty()

    def map_ok(self, fn: Callable[[T_co], U]) -> 'Ok[U]':
        """
        :param fn: The function to apply to the computed value.
        :return: The result of calling ``fn`` on the computed value.
        """
        return Ok(fn(self._o))

    def map_err(self, fn: Any) -> 'Ok[T_co]':
        """
        :param fn: Unused.
        :return: The instance this method was called on, unaltered.
        """
        return self

    def match(self, if_ok: Callable[[T_co], U], if_err: Callable[[E_co], U]) -> U:
        """
        :param if_ok: The function to call on the contained value.
        :param if_err: Unused.
        :return: The result of calling ``if_ok`` on the value.
        """
        return if_ok(self._o)

    def __eq__(self, other: Any) -> bool:
        if type(other) == Ok:
            return self._o == other.ok().unwrap()

        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._o)

    def __repr__(self) -> str:
        return f'Ok({self._o!r})'


@final
class Err(Result[NoReturn, E_co], Generic[E_co]):
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

    def map_ok(self, fn: Any) -> 'Err[E_co]':
        """
        :param fn: Unused.
        :return: The instance this method was called on, unaltered.
        """
        return self

    def map_err(self, fn: Callable[[E_co], F]) -> 'Err[F]':
        """
        :param fn: The function to apply to the error.
        :return: The result of applying ``fn`` the error.
        """
        return Err(fn(self._e))

    def match(self, if_ok: Callable[[T_co], U], if_err: Callable[[E_co], U]) -> U:
        """
        :param if_ok: Unused.
        :param if_err: The function to call on the error.
        :return: The result of calling ``if_err`` on the error.
        """
        return if_err(self._e)

    def __eq__(self, other: Any) -> bool:
        if type(other) == Err:
            return self._e == other.err().unwrap()

        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._e)

    def __repr__(self) -> str:
        return f'Err({self._e!r})'
