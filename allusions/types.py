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
""" Type utilities. """
from typing import TypeVar

T = TypeVar("T")
""" An unbound type variable. """

U = TypeVar('U')
""" An unbound type variable. """

T_co = TypeVar('T_co', covariant=True)
""" An unbound covariant type variable. """
