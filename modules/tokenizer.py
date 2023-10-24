from enum import Enum, auto
from dataclasses import dataclass


class TokenType(Enum):
    EXIT = auto()
    L_PAREN = auto()
    R_PAREN = auto()
    INT_LIT = auto()
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
                else:
                    print("Tokenizing Error: unrecognized value '" + buffer + "'")
                    exit()
            elif self._peek().isnumeric():
                buffer += self._consume()
                while self._peek().isnumeric():
                    buffer += self._consume()
                tokens.append(Token(TokenType.INT_LIT, buffer))
            elif self._peek() == "(":
                tokens.append(Token(TokenType.L_PAREN))
                self._consume()
            elif self._peek() == ")":
                tokens.append(Token(TokenType.R_PAREN))
                self._consume()
            
            else:
                print("Tokenizing Error: unrecognized character '" + self._peek() + "'")
                exit()

        self._index = 0
        return tokens
