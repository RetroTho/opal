from enum import Enum, auto
from dataclasses import dataclass


class TokenType(Enum):
    VARIABLE = auto()
    DATA_TYPE = auto()
    EXIT = auto()
    PRINT = auto()
    IDENT = auto()
    L_PAREN = auto()
    R_PAREN = auto()
    COMMA = auto()
    EQ = auto()
    INT_LIT = auto()
    STR_LIT = auto()
    NEW_LINE = auto()


@dataclass
class Token:
    type: TokenType
    value: str = None


class Tokenizer:
    _index = 0

    def __init__(self, src: str):
        self._src = src

    def _peek(self, offset: int = 0) -> str:
        if self._index + offset < len(self._src):
            return self._src[self._index + offset]
        else:
            return ""

    def _consume(self) -> str:
        self._index += 1
        return self._src[self._index - 1]

    def tokenize(self) -> list[Token]:
        tokens = []
        while self._peek():
            buffer = ""
            if self._peek() == " " or self._peek() == "\t":
                self._consume()
            elif self._peek() == "\n":
                tokens.append(Token(TokenType.NEW_LINE))
                self._consume()
            elif self._peek().isalpha():
                buffer += self._consume()
                while self._peek().isalnum():
                    buffer += self._consume()
                if buffer == "exit":
                    tokens.append(Token(TokenType.EXIT))
                elif buffer == "print":
                    tokens.append(Token(TokenType.PRINT))
                elif buffer == "variable":
                    tokens.append(Token(TokenType.VARIABLE))
                elif buffer == "int":
                    tokens.append(Token(TokenType.DATA_TYPE, buffer))
                elif buffer == "str":
                    tokens.append(Token(TokenType.DATA_TYPE, buffer))
                else:
                    tokens.append(Token(TokenType.IDENT, buffer))
            elif self._peek().isnumeric():
                buffer += self._consume()
                while self._peek().isnumeric():
                    buffer += self._consume()
                tokens.append(Token(TokenType.INT_LIT, buffer))
            elif self._peek() == "'":
                self._consume()
                while self._peek() != "'":
                    buffer += self._consume()
                self._consume()
                tokens.append(Token(TokenType.STR_LIT, buffer))
            elif self._peek() == "(":
                tokens.append(Token(TokenType.L_PAREN))
                self._consume()
            elif self._peek() == ")":
                tokens.append(Token(TokenType.R_PAREN))
                self._consume()
            elif self._peek() == ",":
                tokens.append(Token(TokenType.COMMA))
                self._consume()
            elif self._peek() == "=":
                tokens.append(Token(TokenType.EQ))
                self._consume()
            else:
                print("Tokenizing Error: unrecognized character '" + self._peek() + "'")
                exit()

        self._index = 0
        return tokens
