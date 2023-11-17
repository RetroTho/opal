from modules.tokenizer import Token, TokenType
from modules.parse.nodes import *


class ParseCalls:
    def parseTerm() -> NodeTerm:
        from modules.parse.parse_term import ParseTerm

        return ParseTerm().parse()

    def parseExpr() -> NodeExpr:
        from modules.parse.parse_expr import ParseExpr

        return ParseExpr().parse()

    def parseDetail() -> NodeDetail:
        from modules.parse.parse_detail import ParseDetail

        return ParseDetail().parse()

    def parseScope() -> NodeScope:
        from modules.parse.parse_scope import ParseScope

        return ParseScope().parse()

    def parseStmt() -> NodeStmt:
        from modules.parse.parse_stmt import ParseStmt

        return ParseStmt().parse()

    def parseProg() -> NodeProg:
        from modules.parse.parse_prog import ParseProg

        return ParseProg().parse()


class ParseFuncs:
    def peek(offset: int = 0, type: bool = True) -> Token | TokenType:
        if ParseVars.index + offset < len(ParseVars.tokens):
            if type:
                return ParseVars.tokens[ParseVars.index + offset].type
            else:
                return ParseVars.tokens[ParseVars.index + offset]
        else:
            return None

    def consume() -> Token:
        ParseVars.index += 1
        return ParseVars.tokens[ParseVars.index - 1]

    def binaryPrece(type: TokenType) -> int:
        match type:
            case TokenType.EQ_EQ:
                return 0
            case TokenType.PLUS:
                return 1
            case TokenType.MINUS:
                return 1
            case TokenType.STAR:
                return 2
            case TokenType.F_SLASH:
                return 2
            case _:
                return None


class ParseVars:
    tokens: list[Token] = None
    index: int = 0
