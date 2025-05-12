import inspect
from typing import Callable, List, Optional, Tuple, Any, Union
from typing_extensions import Annotated
from tensorpc import compat
from tensorpc.core.dataclass_dispatch import dataclass
from typing_extensions import TypeAlias, get_type_hints
from dataclasses import Field, make_dataclass, field
import enum 

ValueType: TypeAlias = Union[int, float, str]
NumberType: TypeAlias = Union[int, float]
Vector2Type: TypeAlias = Tuple[float, float]
Vector3Type: TypeAlias = Tuple[float, float, float]

@dataclass
class CommonObject:
    alias: Optional[str] = None
    default: Optional[Any] = None

@dataclass
class Enum:
    alias: Optional[str] = None
    excludes: Optional[List[Any]] = None

@dataclass
class RangedInt:
    lo: int
    hi: int
    step: Optional[int] = None
    alias: Optional[str] = None
    default: Optional[int] = None


@dataclass
class RangedFloat:
    lo: float
    hi: float
    step: Optional[float] = None
    alias: Optional[str] = None
    default: Optional[float] = None


@dataclass
class ColorRGB:
    value_is_string: bool = True
    default: Optional[Union[int, str]] = None


@dataclass
class ColorRGBA:
    value_is_string: bool = True
    default: Optional[Union[int, str]] = None


@dataclass
class RangedVector3:
    lo: float
    hi: float
    step: Optional[float] = None
    alias: Optional[str] = None
    default: Optional[Tuple[float, float, float]] = None

@dataclass
class RangedVector2:
    lo: float
    hi: float
    step: Optional[float] = None
    alias: Optional[str] = None
    default: Optional[Tuple[float, float]] = None

@dataclass
class Vector3:
    step: Optional[float] = None
    alias: Optional[str] = None
    default: Optional[Tuple[float, float, float]] = None

@dataclass
class Vector2:
    step: Optional[float] = None
    alias: Optional[str] = None
    default: Optional[Tuple[float, float]] = None
