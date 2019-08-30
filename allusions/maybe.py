"""
:class:`Maybe` forms the root type of an ADT. Values of type :class:`Maybe` are either instances of :class:`Some` or
:class:`Empty`. As an ADT, this would typically be used with pattern matching, which doesn't exist in Python. Instead,
todo. For example:

    >>> def lookup(key: str, table: Mapping[str, int]) -> Maybe[int]:
    ...     return Some(table[key]) if key in table else Empty
    ...
    >>> animals = {'cat': 1, 'dog': 2}
    >>> lookup('cat', animals).map(str)
    Some('1')
    >>> maybe = lookup('fish', animals).map(str)
    >>> if maybe is Empty:  todo
    ...     print('I wonder where that fish has gone ...')
    I wonder where that fish has gone ...

Aside from ``unwrap``, the API is purely functional.

**Note:** The built-ins :builtin:`type` and :builtin:`isinstance` will not work with `Empty` since it is a value not a
type.
"""
from abc import abstractmethod, ABC
from typing import TypeVar, Generic, NoReturn, Callable, Any, Mapping
from typing_extensions import final, Final

T_co = TypeVar('T_co', covariant=True)
U = TypeVar('U')


class Maybe(ABC, Generic[T_co]):
    """ Container that may or may not contain a value. """
    @abstractmethod
    def unwrap(self) -> T_co:
        """
        :return: The contained value, if it exists.
        :raise ValueError: If the value does not exist.
        """

    @abstractmethod
    def map(self, fn: Callable[[T_co], U]) -> 'Maybe[U]':
        """
        If this is a :class:`Some`, apply the function ``fn`` to the contained value and return it in a :class:`Some`.
        Else return an :class:`Empty`.

        :param fn: The function to apply to the contained value.
        :return: A :class:`Maybe` formed by mapping `fn` over the contained value, if it exists.
        """

    @abstractmethod
    def flat_map(self, fn: Callable[[T_co], 'Maybe[U]']) -> 'Maybe[U]':
        """
        If this is a :class:`Some`, apply the function ``fn`` to the contained value and return the result. Else return
        an :class:`Empty`.

        :param fn: The function to apply to the contained value.
        :return: A :class:`Maybe` formed by mapping `fn` over the contained value, if it exists.
        """

    def match(self, some: Callable[[T_co], U], empty: Callable[[], U]) -> U:
        """
        :param some:
        :param empty:
        :return:
        """


@final
class Some(Maybe[T_co], Generic[T_co]):
    def __init__(self, o: T_co):
        """
        :param o: The value to contain.
        """
        self._o = o

    def unwrap(self) -> T_co:
        """
        :return: The contained value.
        """
        return self._o

    def map(self, fn: Callable[[T_co], U]) -> 'Some[U]':
        """
        :param fn: The function to apply to the contained value.
        :return: A :class:`Some` containing the result of applying ``fn`` to this instance's contained value.
        """
        return Some(fn(self._o))

    def flat_map(self, fn: Callable[[T_co], 'Maybe[U]']) -> 'Maybe[U]':
        """
        :param fn: The function to apply to the contained value.
        :return: The result of applying ``fn`` to the contained value.
        """
        return fn(self._o)

    def match(self, some: Callable[[T_co], U], empty: Callable[[], U]) -> U:
        return some(self._o)

    def __eq__(self, other: Any) -> bool:
        if type(other) == Some:
            return self._o == other.unwrap()

        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._o)

    def __repr__(self) -> str:
        return f'Some({self._o!r})'


@final
class Empty(Maybe[NoReturn]):
    def unwrap(self) -> NoReturn:
        """
        :raise ValueError: Always.
        """
        raise ValueError("No such value.")

    def map(self, fn: Callable[[T_co], U]) -> 'Empty':
        """
        :param fn: Unused.
        :return: An :class:`Empty`.
        """
        return Empty()

    def flat_map(self, fn: Callable[[T_co], 'Maybe[U]']) -> 'Empty':
        """
        :param fn: Unused.
        :return: An :class:`Empty`.
        """
        return Empty()

    def match(self, some: Callable[[NoReturn], U], empty: Callable[[], U]) -> U:
        return empty()

    def __eq__(self, other: Any) -> bool:
        return True if type(other) == Empty else NotImplemented

    def __hash__(self) -> int:
        return 0

    def __repr__(self) -> str:
        return 'Empty()'
