from modules.tokenize.tokens import *
from modules.parse.nodes import *
from modules.parse.common import *


class ParseDetail:
    def _detailReturns(self) -> NodeDetailReturns:
        ParseFuncs.consume()
        if ParseFuncs.peek() == TokenType.L_PAREN:
            ParseFuncs.consume()
        else:
            print("Parsing Error: missing '('")
            exit()
        detail_returns = NodeDetailReturns()
        if ParseFuncs.peek() == TokenType.DATA_TYPE:
            detail_returns.data_type = ParseFuncs.consume()
        else:
            print("Parsing Error: missing data type")
            exit()
        if ParseFuncs.peek() == TokenType.R_PAREN:
            ParseFuncs.consume()
        else:
            print("Parsing Error: missing ')'")
            exit()
        return detail_returns

    def _detailTakes(self) -> NodeDetailTakes:
        ParseFuncs.consume()
        if ParseFuncs.peek() == TokenType.L_PAREN:
            ParseFuncs.consume()
        else:
            print("Parsing Error: missing '('")
            exit()
        detail_takes = NodeDetailTakes()
        if ParseFuncs.peek() == TokenType.DATA_TYPE:
            detail_takes.data_type = ParseFuncs.consume()
        else:
            print("Parsing Error: missing data type")
            exit()
        if ParseFuncs.peek() == TokenType.COMMA:
            ParseFuncs.consume()
        else:
            print("Parsing Error: missing ','")
            exit()
        if ParseFuncs.peek() == TokenType.IDENT:
            detail_takes.ident = ParseFuncs.consume()
        else:
            print("Parsing Error: missing identifier")
            exit()
        if ParseFuncs.peek() == TokenType.R_PAREN:
            ParseFuncs.consume()
        else:
            print("Parsing Error: missing ')'")
            exit()
        return detail_takes

    def parse(self) -> NodeDetail:
        detail_vari = None
        match ParseFuncs.peek():
            case TokenType.D_RETURNS:
                detail_vari = self._detailReturns()
            case TokenType.D_TAKES:
                detail_vari = self._detailTakes()
            case _:
                return None
        detail = NodeDetail()
        detail.vari = detail_vari
        return detail
