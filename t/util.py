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
from collections import deque
from typing import Final


class _A:
    pass


# todo list, set and dict are primitives, no? but they're also collections, so how to sort?
PRIMITIVES: Final[tuple[object, ...]] = (None, True, False, -1, 0, 1, -1., 0., 1., 'a', 'z', '@')

COLLECTIONS: Final[tuple[object, ...]] = (
    tuple(),
    (1, ('a', (True,))),
    list(),
    [1, ['a', [True]]],
    dict(),
    {1: {'a': {True: None}}},
    set(),
    {1, {'a', {True}}},
    frozenset(),
    frozenset({1, {'a', {True}}}),
    deque(),
    deque([1, ['a', [True]]]),
)

EXCEPTIONS: Final[tuple[Exception, ...]] = (Exception(), ValueError(), TypeError(), KeyError())

VALUES: Final[tuple[object, ...]] = PRIMITIVES + EXCEPTIONS + COLLECTIONS + (_A(),)
