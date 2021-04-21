# Copyright 2021 Joel Berkeley
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License
"""
:class:`Maybe` forms the root type of an ADT. Values of type :class:`Maybe` are either instances of
:class:`Some` or class:`Empty`.

Example usage::

    >>> def lookup(key: str, table: Mapping[str, int]) -> Maybe[int]:
    ...     return Some(table[key]) if key in table else Empty()
    ...
    >>> animals = {'cat': 6, 'dog': 3}
    >>> lookup('cat', animals).map(str)
    Some('6')
    >>> lookup('fish', animals).match(
    ...     if_some=lambda count: 'Morning!' * count,
    ...     if_empty=lambda: 'I wonder where that fish has gone ...'
    ... )
    'I wonder where that fish has gone ...'

"""
from __future__ import annotations
from abc import abstractmethod, ABC
from collections.abc import Callable, Mapping
from typing import Generic, NoReturn, cast
from typing_extensions import final

from allusions.types import T_co, U


class Maybe(ABC, Generic[T_co]):
    """ Container that may or may not contain a value. """

    @abstractmethod
    def unwrap(self) -> T_co:
        """
        :return: The contained value, if it exists.
        :raise ValueError: If the value does not exist.
        """

    @abstractmethod
    def map(self, fn: Callable[[T_co], U]) -> Maybe[U]:
        """
        If this is a :class:`Some`, apply the function ``fn`` to the contained value and return it
        in a :class:`Some`. Else return an :class:`Empty`.

        :param fn: The function to apply to the contained value.
        :return: A :class:`Maybe` formed by mapping `fn` over the contained value, if it exists.
        """

    @abstractmethod
    def flat_map(self, fn: Callable[[T_co], Maybe[U]]) -> Maybe[U]:
        """
        If this is a :class:`Some`, apply the function ``fn`` to the contained value and return the
        result. Else return an :class:`Empty`.

        :param fn: The function to apply to the contained value.
        :return: A :class:`Maybe` formed by mapping `fn` over the contained value, if it exists.
        """

    @abstractmethod
    def match(self, *, if_some: Callable[[T_co], U], if_empty: Callable[[], U]) -> U:
        """
        Uses dynamic dispatch to mimic rudimentary pattern matching on this instance. If the
        instance on which this is called contains a value, call ``if_some`` with that value, and
        return its result. Else, call ``if_empty`` and return its result.

        :param if_some: The function to call with the contained value, if it exists.
        :param if_empty: The function to call if the instance is empty.
        :return: The return value of whichever of ``if_some`` and ``if_empty`` were executed.
        """


@final
class Some(Maybe[T_co]):
    """ Implementation of :class:`Maybe` for the case where a value exists. """

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

    def map(self, fn: Callable[[T_co], U]) -> Some[U]:
        """
        :param fn: The function to apply to the contained value.
        :return: A :class:`Some` containing the result of applying ``fn`` to this instance's contained value.
        """
        return Some(fn(self._o))

    def flat_map(self, fn: Callable[[T_co], Maybe[U]]) -> Maybe[U]:
        """
        :param fn: The function to apply to the contained value.
        :return: The result of applying ``fn`` to the contained value.
        """
        return fn(self._o)

    def match(self, *, if_some: Callable[[T_co], U], if_empty: Callable[[], U]) -> U:
        """
        :param if_some: The function to apply to the contained value.
        :param if_empty: Unused.
        :return: The result of calling ``if_some`` on the contained value.
        """
        return if_some(self._o)

    def __eq__(self, other: object) -> bool:
        if type(other) == Some:
            return self._o == cast(Some, other).unwrap()

        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._o)

    def __repr__(self) -> str:
        return f"Some({self._o!r})"


@final
class Empty(Maybe[NoReturn]):
    """ Implementation of :class:`Maybe` for the case where no value exists. """

    def unwrap(self) -> NoReturn:
        """
        :raise ValueError: Always.
        """
        raise ValueError("No such value.")

    def map(self, fn: Callable[[T_co], U]) -> Empty:
        """
        :param fn: Unused.
        :return: An :class:`Empty`.
        """
        return Empty()

    def flat_map(self, fn: Callable[[T_co], Maybe[U]]) -> Empty:
        """
        :param fn: Unused.
        :return: An :class:`Empty`.
        """
        return Empty()

    def match(self, *, if_some: Callable[[NoReturn], U], if_empty: Callable[[], U]) -> U:
        """
        :param if_some: Unused.
        :param if_empty: The function to call.
        :return: The return value of ``if_empty``.
        """
        return if_empty()

    def __eq__(self, other: object) -> bool:
        if type(other) == Empty:
            return True

        return NotImplemented

    def __hash__(self) -> int:
        return 0

    def __repr__(self) -> str:
        return "Empty()"
