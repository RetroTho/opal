from __future__ import annotations
from dataclasses import dataclass
from modules.tokenizer import Token, TokenType


@dataclass
class NodeTermIntLit:
    int_lit: Token = None  # INT_LIT


@dataclass
class NodeTermStrLit:
    str_lit: Token = None  # STR_LIT


@dataclass
class NodeTermIdent:
    ident: Token = None  # Ident


@dataclass
class NodeTermParen:
    expr: NodeExpr = None


@dataclass
class NodeTerm:
    vari: NodeTermIntLit | NodeTermStrLit | NodeTermParen = None


@dataclass
class NodeBinaryExprAdd:
    left: NodeExpr = None
    right: NodeExpr = None


@dataclass
class NodeBinaryExprSub:
    left: NodeExpr = None
    right: NodeExpr = None


@dataclass
class NodeBinaryExprMult:
    left: NodeExpr = None
    right: NodeExpr = None


@dataclass
class NodeBinaryExprDiv:
    left: NodeExpr = None
    right: NodeExpr = None


@dataclass
class NodeBinaryExpr:
    vari: NodeBinaryExprAdd | NodeBinaryExprSub | NodeBinaryExprMult | NodeBinaryExprDiv = (
        None
    )


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
class NodeStmtVariable:
    ident: Token = None  # IDENT
    data_type: Token = None  # DATA_TYPE
    expr: NodeExpr = None


@dataclass
class NodeStmtIdent:
    ident: Token = None  # IDENT
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

    def _consume(self) -> Token:
        self._index += 1
        return self._tokens[self._index - 1]

    def _binaryPrece(self, type: TokenType) -> int:
        match type:
            case TokenType.PLUS:
                return 0
            case TokenType.MINUS:
                return 0
            case TokenType.STAR:
                return 1
            case TokenType.F_SLASH:
                return 1
            case _:
                return None

    def _parseTerm(self) -> NodeTerm:
        if self._peek() == TokenType.INT_LIT:
            term_int_lit = NodeTermIntLit()
            term_int_lit.int_lit = self._consume()
            term = NodeTerm()
            term.vari = term_int_lit
            return term
        elif self._peek() == TokenType.STR_LIT:
            term_str_lit = NodeTermStrLit()
            term_str_lit.str_lit = self._consume()
            term = NodeTerm()
            term.vari = term_str_lit
            return term
        elif self._peek() == TokenType.IDENT:
            term_ident = NodeTermIdent()
            term_ident.ident = self._consume()
            term = NodeTerm()
            term.vari = term_ident
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

    def _parseExpr(self, min_prece: int = 0) -> NodeExpr:
        term_left = self._parseTerm()
        if term_left is None:
            return None
        expr = NodeExpr()
        expr.vari = term_left
        while True:
            curr_token_type = self._peek()
            if curr_token_type is not None:
                prece = self._binaryPrece(curr_token_type)
                if (prece is None) or (prece < min_prece):
                    break
            else:
                break
            op = self._consume()
            next_min_prece = prece + 1
            expr_right = self._parseExpr(next_min_prece)
            if expr_right is None:
                print("Parsing Error: invalid expression")
                exit()
            binary_expr = NodeBinaryExpr()
            expr_left = NodeExpr()
            if op.type == TokenType.PLUS:
                add = NodeBinaryExprAdd()
                expr_left.vari = expr.vari
                add.left = expr_left
                add.right = expr_right
                binary_expr.vari = add
            elif op.type == TokenType.MINUS:
                sub = NodeBinaryExprSub()
                expr_left.vari = expr.vari
                sub.left = expr_left
                sub.right = expr_right
                binary_expr.vari = sub
            elif op.type == TokenType.STAR:
                mult = NodeBinaryExprMult()
                expr_left.vari = expr.vari
                mult.left = expr_left
                mult.right = expr_right
                binary_expr.vari = mult
            elif op.type == TokenType.F_SLASH:
                div = NodeBinaryExprDiv()
                expr_left.vari = expr.vari
                div.left = expr_left
                div.right = expr_right
                binary_expr.vari = div
            else:
                print("Parsing Error: invalid binary operator")
                exit()
            expr.vari = binary_expr
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
            if expr is None or not isinstance(expr.vari.vari, NodeTermIntLit):
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
        elif self._peek() == TokenType.VARIABLE:
            self._consume()
            stmt_variable = NodeStmtVariable()
            if self._peek() == TokenType.IDENT:
                stmt_variable.ident = self._consume()
            else:
                print("Parsing Error: missing identifier")
                exit()
            if self._peek() == TokenType.L_PAREN:
                self._consume()
            else:
                print("Parsing Error: missing '('")
                exit()
            if self._peek() == TokenType.DATA_TYPE:
                stmt_variable.data_type = self._consume()
            else:
                print("Parsing Error: missing data type")
                exit()
            if self._peek() == TokenType.COMMA:
                self._consume()
                expr = self._parseExpr()
                if expr is None:
                    print("Parsing Error: invalid expression")
                    exit()
                stmt_variable.expr = expr
            elif self._peek() != TokenType.R_PAREN:
                print("Parsing Error: missing ','")
                exit()
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
            stmt.vari = stmt_variable
            return stmt
        elif self._peek() == TokenType.IDENT:
            stmt_ident = NodeStmtIdent()
            stmt_ident.ident = self._consume()
            if self._peek() == TokenType.EQ:
                self._consume()
            else:
                print("Parsing Error: unexpected identifier")
                exit()
            expr = self._parseExpr()
            if expr is None:
                print("Parsing Error: invalid expression")
                exit()
            stmt_ident.expr = expr
            if self._peek() == TokenType.NEW_LINE or self._peek() is None:
                if self._peek() is not None:
                    self._consume()
            else:
                print("Parsing Error: issue ending statement")
                exit()
            stmt = NodeStmt()
            stmt.vari = stmt_ident
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
