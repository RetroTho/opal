from enum import Enum, auto
from dataclasses import dataclass

class DataType(Enum):
    INT = auto()
    STR = auto()


@dataclass
class Variable:
    name: str
    type: DataType


@dataclass
class Function:
    name: str
    return_type: DataType
    args: list[Variable]