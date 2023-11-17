from modules.tokenizer import TokenType
from modules.parse.nodes import *
from modules.parse.common import *


class ParseScope:
    def parse(self) -> NodeScope:
        if ParseFuncs.peek() == TokenType.L_CURLY:
            ParseFuncs.consume()
        else:
            print("Parsing Error: missing '{'")
            exit()
        if ParseFuncs.peek() == TokenType.NEW_LINE:
            ParseFuncs.consume()
        scope = NodeScope()
        scope.stmts = []
        while True:
            stmt = ParseCalls.parseStmt()
            if stmt is None:
                break
            scope.stmts.append(stmt)
        if ParseFuncs.peek() == TokenType.R_CURLY:
            ParseFuncs.consume()
        else:
            print("Parsing Error: missing '}'")
            exit()
        return scope
