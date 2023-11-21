from modules.tokenize.common import *
from modules.tokenize.tokens import *


class Tokenizer:
    def __init__(self, src: str):
        TokVars.src = src

    def _matchIsAlpha(self, buffer) -> Token:
        match buffer:
            case "exit":
                return Token(TokenType.EXIT)
            case "return":
                return Token(TokenType.RETURN)
            case "print":
                return Token(TokenType.PRINT)
            case "if":
                return Token(TokenType.IF)
            case "while":
                return Token(TokenType.WHILE)
            case "variable":
                return Token(TokenType.VARIABLE)
            case "function":
                return Token(TokenType.FUNCTION)
            case "returns":
                return Token(TokenType.D_RETURNS)
            case "takes":
                return Token(TokenType.D_TAKES)
            case "int":
                return Token(TokenType.DATA_TYPE, buffer)
            case "str":
                return Token(TokenType.DATA_TYPE, buffer)
            case _:
                return Token(TokenType.IDENT, buffer)

    def tokenize(self) -> list[Token]:
        tokens = []
        while TokFuncs.peek() is not None:
            buffer = ""
            char = TokFuncs.peek()
            match char:
                case " ":
                    TokFuncs.consume()
                case "\t":
                    TokFuncs.consume()
                case "\n":
                    TokFuncs.consume()
                    tokens.append(Token(TokenType.NEW_LINE))
                case "'":
                    TokFuncs.consume()
                    while TokFuncs.peek() != "'":
                        buffer += TokFuncs.consume()
                    TokFuncs.consume()
                    tokens.append(Token(TokenType.STR_LIT, buffer))
                case "(":
                    TokFuncs.consume()
                    tokens.append(Token(TokenType.L_PAREN))
                case ")":
                    TokFuncs.consume()
                    tokens.append(Token(TokenType.R_PAREN))
                case "{":
                    TokFuncs.consume()
                    tokens.append(Token(TokenType.L_CURLY))
                case "}":
                    TokFuncs.consume()
                    tokens.append(Token(TokenType.R_CURLY))
                case ",":
                    TokFuncs.consume()
                    tokens.append(Token(TokenType.COMMA))
                case "=":
                    TokFuncs.consume()
                    if TokFuncs.peek() == "=":
                        TokFuncs.consume()
                        tokens.append(Token(TokenType.EQ_EQ))
                    else:
                        tokens.append(Token(TokenType.EQ))
                case "+":
                    TokFuncs.consume()
                    tokens.append(Token(TokenType.PLUS))
                case "-":
                    TokFuncs.consume()
                    tokens.append(Token(TokenType.MINUS))
                case "*":
                    TokFuncs.consume()
                    tokens.append(Token(TokenType.STAR))
                case "/":
                    TokFuncs.consume()
                    tokens.append(Token(TokenType.F_SLASH))
                case _:
                    if char.isalpha():
                        buffer += TokFuncs.consume()
                        while TokFuncs.peek().isalnum():
                            buffer += TokFuncs.consume()
                        tokens.append(self._matchIsAlpha(buffer))
                    elif char.isnumeric():
                        buffer += TokFuncs.consume()
                        while TokFuncs.peek().isnumeric():
                            buffer += TokFuncs.consume()
                        tokens.append(Token(TokenType.INT_LIT, buffer))
                    else:
                        print(
                            "Tokenizing Error: unrecognized character '"
                            + TokFuncs.peek()
                            + "'"
                        )
                        exit()

        return tokens
