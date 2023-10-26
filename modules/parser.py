from __future__ import annotations
from dataclasses import dataclass
from modules.tokenizer import Token, TokenType


@dataclass
class NodeTermIntLit:
    int_lit: Token = None  # INT_LIT


@dataclass
class NodeTermParen:
    expr: NodeExpr = None


@dataclass
class NodeTerm:
    vari: NodeTermIntLit = None


@dataclass
class NodeExpr:
    vari: NodeTerm = None


@dataclass
class NodeStmtExit:
    expr: NodeExpr = None


@dataclass
class NodeStmtPrint:
    expr: NodeExpr = None


@dataclass
class NodeStmt:
    vari: NodeStmtExit = None


@dataclass
class NodeProg:
    stmts: list[NodeStmt] = None


class Parser:
    _index = 0

    def __init__(self, tokens: list[Token]):
        self._tokens = tokens

    def _peek(self, type: bool = True, offset: int = 0) -> Token | TokenType:
        if self._index + offset < len(self._tokens):
            if type:
                return self._tokens[self._index + offset].type
            else:
                return self._tokens[self._index + offset]
        else:
            return None

    def _peekType(self, offset: int = 0) -> Token:
        if self._index + offset < len(self._tokens):
            return self._tokens[self._index + offset]
        else:
            return None

    def _consume(self) -> Token:
        self._index += 1
        return self._tokens[self._index - 1]

    def _parseTerm(self) -> NodeTerm:
        if self._peek() == TokenType.INT_LIT:
            term_int_lit = NodeTermIntLit()
            term_int_lit.int_lit = self._consume()
            term = NodeTerm()
            term.vari = term_int_lit
            return term
        elif self._peek() == TokenType.L_PAREN:
            self._consume()
            expr = self._parseExpr()
            if expr is None:
                print("Parsing Error: invalid expression")
                exit()
            if self._peek() == TokenType.R_PAREN:
                self._consume()
            else:
                print("Parsing Error: missing ')'")
                exit()
            term_paren = NodeTermParen()
            term_paren.expr = expr
            term = NodeTerm()
            term.vari = term_paren
            return term
        else:
            return None

    def _parseExpr(self) -> NodeExpr:
        term = self._parseTerm()
        if term is None:
            return None
        expr = NodeExpr()
        expr.vari = term
        return expr

    def _parseStmt(self) -> NodeStmt:
        if self._peek() == TokenType.EXIT:
            self._consume()
            if self._peek() == TokenType.L_PAREN:
                self._consume()
            else:
                print("Parsing Error: missing '('")
                exit()
            stmt_exit = NodeStmtExit()
            expr = self._parseExpr()
            if expr is None:
                print("Parsing Error: invalid expression")
                exit()
            stmt_exit.expr = expr
            if self._peek() == TokenType.R_PAREN:
                self._consume()
            else:
                print("Parsing Error: missing ')'")
                exit()
            if self._peek() == TokenType.NEW_LINE or self._peek() is None:
                if self._peek() is not None:
                    self._consume()
            else:
                print("Parsing Error: issue ending statement")
                exit()
            stmt = NodeStmt()
            stmt.vari = stmt_exit
            return stmt
        elif self._peek() == TokenType.PRINT:
            self._consume()
            if self._peek() == TokenType.L_PAREN:
                self._consume()
            else:
                print("Parsing Error: missing '('")
                exit()
            stmt_print = NodeStmtPrint()
            expr = self._parseExpr()
            if expr is None:
                print("Parsing Error: invalid expression")
                exit()
            stmt_print.expr = expr
            if self._peek() == TokenType.R_PAREN:
                self._consume()
            else:
                print("Parsing Error: missing ')'")
                exit()
            if self._peek() == TokenType.NEW_LINE or self._peek() is None:
                if self._peek() is not None:
                    self._consume()
            else:
                print("Parsing Error: issue ending statement")
                exit()
            stmt = NodeStmt()
            stmt.vari = stmt_print
            return stmt
        else:
            return None

    def _parseProg(self) -> NodeProg:
        prog = NodeProg()
        prog.stmts = []
        while self._peek() != None:
            stmt = self._parseStmt()
            if stmt != None:
                prog.stmts.append(stmt)
            else:
                print("Parsing Error: invalid statement")
                exit()
        return prog

    def parse(self) -> NodeProg:
        return self._parseProg()
