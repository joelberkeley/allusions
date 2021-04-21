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
from __future__ import annotations
from collections.abc import Hashable
from typing import Final

COLLECTIONS: Final[tuple[object, ...]] = (
    (1, ('a', ())),
    [1, ['a', []]],
    {1: {'a': {}}},
    {1, 'a', frozenset()},
)
""" A selection of collections. """


class _A:
    pass


VALUES: Final[tuple[object, ...]] = (
    _A(),
    None,
    True,
    -1.2,
    'a',
    Exception(),
) + COLLECTIONS
""" Values of a wide variety of types. """


def is_hashable(o: object) -> bool:
    """
    :param o: An object.
    :return: `True` if ``o`` is hashable, else `False`.
    """
    return isinstance(o, Hashable)
