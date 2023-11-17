from modules.tokenizer import TokenType
from modules.parse.nodes import *
from modules.parse.common import *


class ParseProg:
    def parse(self) -> NodeProg:
        prog = NodeProg()
        prog.stmts = []
        while ParseFuncs.peek() is not None:
            if ParseFuncs.peek() == TokenType.NEW_LINE:
                ParseFuncs.consume()
                continue
            stmt = ParseCalls.parseStmt()
            if stmt is not None:
                prog.stmts.append(stmt)
            else:
                print("Parsing Error: invalid statement")
                exit()
        return prog
