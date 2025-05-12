from typing import (TYPE_CHECKING, Any, AsyncGenerator, Awaitable, Callable,
                    Coroutine, Dict, Generic, Iterable, List, Optional, Set,
                    Tuple, Type, TypeVar, Union)
from pydantic_core import core_schema
from pydantic import (
    GetCoreSchemaHandler, )
from typing_extensions import Self

_LENGTH_SPLIT = "."

class UniqueTreeId:
    # format: length1,length2,length3|part1::part2::part3
    # part names may contains splitter '::', so we need lengths to split
    # splitter is only used for better readability, it's not necessary.
    def __init__(self, uid: str, splitter_length: int = 1) -> None:
        self.uid_encoded = uid
        # init_parts = uid.split("|")
        splitter_first_index = uid.find("|")
        if splitter_first_index == -1:
            # empty uid, means uid must be ""
            assert len(
                uid
            ) == 0, f"uid should be empty if no splitter exists, but got {uid}"
            self.parts: List[str] = []
            uid_part = ""
            lengths: List[int] = []
        else:
            length_part = uid[:splitter_first_index]
            uid_part = uid[splitter_first_index + 1:]
            lengths = [int(n) for n in length_part.split(_LENGTH_SPLIT)]
            assert sum(lengths) == len(uid_part) - splitter_length * (
                len(lengths) - 1), f"{uid} not valid, {lengths}, {uid_part}"
        start = 0
        self.parts: List[str] = []
        for l in lengths:
            self.parts.append(uid_part[start:start + l])
            start += l + splitter_length
        self.splitter_length = splitter_length

    def empty(self):
        return len(self.uid_encoded) == 0

    def set_parts_inplace(self, parts: List[str], splitter: str = "."):
        self.parts = parts
        self.uid_encoded = _LENGTH_SPLIT.join([str(len(p)) for p in parts]) + "|" + splitter.join(parts)

    @classmethod
    def from_parts(cls,
                   parts: List[str],
                   splitter: str = "."):
        if len(parts) == 0:
            return cls("", len(splitter))
        return cls(
            _LENGTH_SPLIT.join([str(len(p))
                      for p in parts]) + "|" + splitter.join(parts),
            len(splitter))

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.uid_encoded})"

    def __hash__(self) -> int:
        return hash(self.uid_encoded)

    def append_part(self, part: str, splitter: str = ".") -> Self:
        return self.__class__.from_parts(self.parts + [part], splitter)

    def extend_parts(self, parts: List[str], splitter: str = ".") -> Self:
        return self.__class__.from_parts(self.parts + parts, splitter)

    def pop(self):
        return self.__class__.from_parts(self.parts[:-1])

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, UniqueTreeId):
            return False
        return self.uid_encoded == o.uid_encoded

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

    def __add__(self, other: Union[Self, str]) -> Self:
        if isinstance(other, str):
            return self.__class__.from_parts(self.parts + [other], ".")
        return self.__class__.from_parts(self.parts + other.parts, ".")

    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type: Any,
                                     _handler: GetCoreSchemaHandler):
        return core_schema.no_info_after_validator_function(
            cls.validate,
            core_schema.any_schema(),
        )

    @classmethod
    def validate(cls, v):
        if isinstance(v, str):
            return UniqueTreeId(v)
        if not isinstance(v, UniqueTreeId):
            raise ValueError('undefined required, but get', type(v))
        return v

    def startswith(self, other: Self) -> bool:
        if len(self.parts) < len(other.parts):
            return False
        for i in range(len(other.parts)):
            if self.parts[i] != other.parts[i]:
                return False
        return True

    def common_prefix(self, other: Self) -> Self:
        i = 0
        while i < len(self.parts) and i < len(
                other.parts) and self.parts[i] == other.parts[i]:
            i += 1
        return self.__class__.from_parts(self.parts[:i])

    def common_prefix_index(self, other: Self) -> int:
        i = 0
        while i < len(self.parts) and i < len(
                other.parts) and self.parts[i] == other.parts[i]:
            i += 1
        return i

    def copy(self) -> Self:
        return self.__class__(self.uid_encoded, self.splitter_length)

class UniqueTreeIdForComp(UniqueTreeId):
    pass 

class UniqueTreeIdForTree(UniqueTreeId):

    @classmethod
    def from_parts(cls,
                   parts: List[str],
                   splitter: str = ".") -> "UniqueTreeIdForTree":
        if len(parts) == 0:
            return cls("", len(splitter))
        return cls(
            _LENGTH_SPLIT.join([str(len(p))
                      for p in parts]) + "|" + splitter.join(parts),
            len(splitter))

    def append_part(self,
                    part: str,
                    splitter: str = ".") -> "UniqueTreeIdForTree":
        return UniqueTreeIdForTree.from_parts(self.parts + [part], splitter)

    def extend_parts(self, parts: List[str], splitter: str = ".") -> "UniqueTreeIdForTree":
        return UniqueTreeIdForTree.from_parts(self.parts + parts, splitter)

    def pop(self):
        return UniqueTreeIdForTree.from_parts(self.parts[:-1])

    def __add__(
            self, other: Union["UniqueTreeIdForTree", UniqueTreeId,
                               str]) -> "UniqueTreeIdForTree":
        if isinstance(other, str):
            return UniqueTreeIdForTree.from_parts(self.parts + [other], ".")
        return UniqueTreeIdForTree.from_parts(self.parts + other.parts, ".")

    def copy(self) -> "UniqueTreeIdForTree":
        return UniqueTreeIdForTree(self.uid_encoded, self.splitter_length)