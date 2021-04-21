from __future__ import annotations

from typing import TypeVar, Any


ClassType = TypeVar("ClassType", bound=type)


class ADT:
    def __class_getitem__(cls, item: str | tuple[str, ...]):
        ...

    def __new__(cls: ClassType, *args: Any, **kwargs: Any) -> ClassType:
        ...
