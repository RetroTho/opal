from modules.tokenize.tokens import *
from modules.parse.nodes import *
from modules.parse.common import *


class ParseTerm:
    def _termIdent(self) -> NodeTermFuncCall | NodeTermVar:
        if ParseFuncs.peek(1) == TokenType.L_PAREN:
            term_ident = NodeTermFuncCall()
            term_ident.ident = ParseFuncs.consume()
            ParseFuncs.consume()
            exprs = []
            expr = ParseCalls.parseExpr()
            if expr is not None:
                exprs.append(expr)
                while ParseFuncs.peek() == TokenType.COMMA:
                    ParseFuncs.consume()
                    expr = ParseCalls.parseExpr()
                    if expr is not None:
                        exprs.append(expr)
                    else:
                        print("Parsing Error: invalid expression")
                        exit()
            term_ident.exprs = exprs
            if ParseFuncs.peek() == TokenType.R_PAREN:
                ParseFuncs.consume()
            else:
                print("Parsing Error: missing ')'")
                exit()
        else:
            term_ident = NodeTermVar()
            term_ident.ident = ParseFuncs.consume()
        return term_ident

    def _termParen(self) -> NodeTermParen():
        ParseFuncs.consume()
        expr = ParseCalls.parseExpr()
        if expr is None:
            print("Parsing Error: invalid expression")
            exit()
        if ParseFuncs.peek() == TokenType.R_PAREN:
            ParseFuncs.consume()
        else:
            print("Parsing Error: missing ')'")
            exit()
        term_paren = NodeTermParen()
        term_paren.expr = expr
        return term_paren

    def parse(self) -> NodeTerm:
        term_vari = None
        match ParseFuncs.peek():
            case TokenType.INT_LIT:
                term_vari = NodeTermIntLit()
                term_vari.int_lit = ParseFuncs.consume()
            case TokenType.STR_LIT:
                term_vari = NodeTermStrLit()
                term_vari.str_lit = ParseFuncs.consume()
            case TokenType.IDENT:
                term_vari = self._termIdent()
            case TokenType.L_PAREN:
                term_vari = self._termParen()
            case _:
                return None
        term = NodeTerm()
        term.vari = term_vari
        return term
