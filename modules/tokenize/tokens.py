from enum import Enum, auto
from dataclasses import dataclass


class TokenType(Enum):
    VARIABLE = auto()
    FUNCTION = auto()
    D_RETURNS = auto()
    D_TAKES = auto()
    DATA_TYPE = auto()
    EXIT = auto()
    RETURN = auto()
    PRINT = auto()
    IF = auto()
    WHILE = auto()
    IDENT = auto()
    L_PAREN = auto()
    R_PAREN = auto()
    L_CURLY = auto()
    R_CURLY = auto()
    COMMA = auto()
    EQ = auto()
    EQ_EQ = auto()
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    F_SLASH = auto()
    INT_LIT = auto()
    STR_LIT = auto()
    NEW_LINE = auto()


@dataclass
class Token:
    type: TokenType
    value: str = None
