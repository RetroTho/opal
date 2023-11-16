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
class NodeTermVar:
    ident: Token = None  # IDENT


@dataclass
class NodeTermFuncCall:
    ident: Token = None  # IDENT
    exprs: list[NodeExpr] = None


@dataclass
class NodeTermParen:
    expr: NodeExpr = None


@dataclass
class NodeTerm:
    vari: (
        NodeTermIntLit | NodeTermStrLit | NodeTermVar | NodeTermFuncCall | NodeTermParen
    ) = None


@dataclass
class NodeBinaryExprIsEq:
    left: NodeExpr = None
    right: NodeExpr = None


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
    vari: (
        NodeBinaryExprIsEq
        | NodeBinaryExprAdd
        | NodeBinaryExprSub
        | NodeBinaryExprMult
        | NodeBinaryExprDiv
    ) = None


@dataclass
class NodeExpr:
    vari: (NodeTerm | NodeBinaryExpr) = None


@dataclass
class NodeDetailReturns:
    data_type: Token = None  # DATA_TYPE


@dataclass
class NodeDetailTakes:
    data_type: Token = None  # DATA_TYPE
    ident: Token = None  # IDENT


@dataclass
class NodeDetail:
    vari: (NodeDetailReturns | NodeDetailTakes) = None


@dataclass
class NodeStmtExit:
    expr: NodeExpr = None


@dataclass
class NodeStmtReturn:
    expr: NodeExpr = None


@dataclass
class NodeStmtPrint:
    expr: NodeExpr = None


@dataclass
class NodeStmtIf:
    expr: NodeExpr = None
    scope: NodeScope = None


@dataclass
class NodeStmtWhile:
    expr: NodeExpr = None
    scope: NodeScope = None


@dataclass
class NodeStmtVariable:
    ident: Token = None  # IDENT
    data_type: Token = None  # DATA_TYPE
    expr: NodeExpr = None


@dataclass
class NodeStmtFunction:
    ident: Token = None  # IDENT
    takes: list[NodeDetail] = None
    returns: NodeDetail = None
    scope: NodeScope = None


@dataclass
class NodeStmtFuncCall:
    ident: Token = None  # IDENT
    exprs: list[NodeExpr] = None


@dataclass
class NodeStmtVarAssign:
    ident: Token = None  # IDENT
    expr: NodeExpr = None


@dataclass
class NodeStmt:
    vari: (
        NodeStmtExit
        | NodeStmtReturn
        | NodeStmtPrint
        | NodeStmtIf
        | NodeStmtWhile
        | NodeStmtVariable
        | NodeStmtFunction
        | NodeStmtFuncCall
        | NodeStmtVarAssign
    ) = None


@dataclass
class NodeScope:
    stmts: list[NodeStmt] = None


@dataclass
class NodeProg:
    stmts: list[NodeStmt] = None


class Parser:
    def __init__(self, tokens: list[Token]):
        self._tokens = tokens
        self._index = 0

    def _peek(self, offset: int = 0, type: bool = True) -> Token | TokenType:
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
            if self._peek(1) == TokenType.L_PAREN:
                term_ident = NodeTermFuncCall()
                term_ident.ident = self._consume()
                self._consume()
                exprs = []
                expr = self._parseExpr()
                if expr is not None:
                    exprs.append(expr)
                    while self._peek() == TokenType.COMMA:
                        self._consume()
                        expr = self._parseExpr()
                        if expr is not None:
                            exprs.append(expr)
                        else:
                            print("Parsing Error: invalid expression")
                            exit()
                term_ident.exprs = exprs
                if self._peek() == TokenType.R_PAREN:
                    self._consume()
                else:
                    print("Parsing Error: missing ')'")
                    exit()
            else:
                term_ident = NodeTermVar()
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
            if op.type == TokenType.EQ_EQ:
                is_eq = NodeBinaryExprIsEq()
                expr_left.vari = expr.vari
                is_eq.left = expr_left
                is_eq.right = expr_right
                binary_expr.vari = is_eq
            elif op.type == TokenType.PLUS:
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

    def _parseDetail(self) -> NodeDetail:
        if self._peek() == TokenType.D_RETURNS:
            self._consume()
            if self._peek() == TokenType.L_PAREN:
                self._consume()
            else:
                print("Parsing Error: missing '('")
                exit()
            detail_returns = NodeDetailReturns()
            if self._peek() == TokenType.DATA_TYPE:
                detail_returns.data_type = self._consume()
            else:
                print("Parsing Error: missing data type")
                exit()
            if self._peek() == TokenType.R_PAREN:
                self._consume()
            else:
                print("Parsing Error: missing ')'")
                exit()
            detail = NodeDetail()
            detail.vari = detail_returns
            return detail
        elif self._peek() == TokenType.D_TAKES:
            self._consume()
            if self._peek() == TokenType.L_PAREN:
                self._consume()
            else:
                print("Parsing Error: missing '('")
                exit()
            detail_takes = NodeDetailTakes()
            if self._peek() == TokenType.DATA_TYPE:
                detail_takes.data_type = self._consume()
            else:
                print("Parsing Error: missing data type")
                exit()
            if self._peek() == TokenType.COMMA:
                self._consume()
            else:
                print("Parsing Error: missing ','")
                exit()
            if self._peek() == TokenType.IDENT:
                detail_takes.ident = self._consume()
            else:
                print("Parsing Error: missing identifier")
                exit()
            if self._peek() == TokenType.R_PAREN:
                self._consume()
            else:
                print("Parsing Error: missing ')'")
                exit()
            detail = NodeDetail()
            detail.vari = detail_takes
            return detail
        else:
            return None

    def _parseScope(self) -> NodeScope:
        if self._peek() == TokenType.L_CURLY:
            self._consume()
        else:
            print("Parsing Error: missing '{'")
            exit()
        if self._peek() == TokenType.NEW_LINE:
            self._consume()
        scope = NodeScope()
        scope.stmts = []
        while True:
            stmt = self._parseStmt()
            if stmt is None:
                break
            scope.stmts.append(stmt)
        if self._peek() == TokenType.R_CURLY:
            self._consume()
        else:
            print("Parsing Error: missing '}'")
            exit()
        return scope

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
        elif self._peek() == TokenType.RETURN:
            self._consume()
            if self._peek() == TokenType.L_PAREN:
                self._consume()
            else:
                print("Parsing Error: missing '('")
                exit()
            stmt_return = NodeStmtReturn()
            expr = self._parseExpr()
            if expr is None:
                print("Parsing Error: invalid expression")
                exit()
            stmt_return.expr = expr
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
            stmt.vari = stmt_return
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
        elif self._peek() == TokenType.IF:
            self._consume()
            if self._peek() == TokenType.L_PAREN:
                self._consume()
            else:
                print("Parsing Error: missing '('")
                exit()
            stmt_if = NodeStmtIf()
            expr = self._parseExpr()
            if expr is None:
                print("Parsing Error: invalid expression")
                exit()
            stmt_if.expr = expr
            if self._peek() == TokenType.R_PAREN:
                self._consume()
            else:
                print("Parsing Error: missing ')'")
                exit()
            stmt_if.scope = self._parseScope()
            if self._peek() == TokenType.NEW_LINE or self._peek() is None:
                if self._peek() is not None:
                    self._consume()
            else:
                print("Parsing Error: issue ending statement")
                exit()
            stmt = NodeStmt()
            stmt.vari = stmt_if
            return stmt
        elif self._peek() == TokenType.WHILE:
            self._consume()
            if self._peek() == TokenType.L_PAREN:
                self._consume()
            else:
                print("Parsing Error: missing '('")
                exit()
            stmt_while = NodeStmtWhile()
            expr = self._parseExpr()
            if expr is None:
                print("Parsing Error: invalid expression")
                exit()
            stmt_while.expr = expr
            if self._peek() == TokenType.R_PAREN:
                self._consume()
            else:
                print("Parsing Error: missing ')'")
                exit()
            stmt_while.scope = self._parseScope()
            if self._peek() == TokenType.NEW_LINE or self._peek() is None:
                if self._peek() is not None:
                    self._consume()
            else:
                print("Parsing Error: issue ending statement")
                exit()
            stmt = NodeStmt()
            stmt.vari = stmt_while
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
        elif self._peek() == TokenType.FUNCTION:
            self._consume()
            stmt_function = NodeStmtFunction()
            if self._peek() == TokenType.IDENT:
                stmt_function.ident = self._consume()
            else:
                print("Parsing Error: missing identifier")
                exit()
            if self._peek() == TokenType.L_PAREN:
                self._consume()
            else:
                print("Parsing Error: missing '('")
                exit()
            if self._peek() == TokenType.NEW_LINE:
                self._consume()
            returns = False
            first = True
            while (
                self._peek() == TokenType.D_RETURNS
                or self._peek() == TokenType.D_TAKES
                or self._peek() == TokenType.COMMA
            ):
                if first:
                    first = False
                else:
                    if self._peek() == TokenType.COMMA:
                        self._consume()
                    else:
                        print("Parsing Error: missing ','")
                        exit()
                    if self._peek() == TokenType.NEW_LINE:
                        self._consume()
                if self._peek() == TokenType.D_RETURNS:
                    if not returns:
                        stmt_function.returns = self._parseDetail()
                        returns = True
                    else:
                        print("Parsing Error: return type already set")
                        exit()
                elif self._peek() == TokenType.D_TAKES:
                    if stmt_function.takes is None:
                        stmt_function.takes = []
                    stmt_function.takes.append(self._parseDetail())
                if self._peek() == TokenType.NEW_LINE:
                    self._consume()
            if self._peek() == TokenType.R_PAREN:
                self._consume()
            else:
                print("Parsing Error: missing ')'")
                exit()
            stmt_function.scope = self._parseScope()
            if self._peek() == TokenType.NEW_LINE or self._peek() is None:
                if self._peek() is not None:
                    self._consume()
            else:
                print("Parsing Error: issue ending statement")
                exit()
            stmt = NodeStmt()
            stmt.vari = stmt_function
            return stmt
        elif self._peek() == TokenType.IDENT:
            if self._peek(1) == TokenType.EQ:
                stmt_ident = NodeStmtVarAssign()
                stmt_ident.ident = self._consume()
                self._consume()
                expr = self._parseExpr()
                if expr is None:
                    print("Parsing Error: invalid expression")
                    exit()
                stmt_ident.expr = expr
            elif self._peek(1) == TokenType.L_PAREN:
                stmt_ident = NodeStmtFuncCall()
                stmt_ident.ident = self._consume()
                self._consume()
                exprs = []
                expr = self._parseExpr()
                if expr is not None:
                    exprs.append(expr)
                    while self._peek() == TokenType.COMMA:
                        self._consume()
                        expr = self._parseExpr()
                        if expr is not None:
                            exprs.append(expr)
                        else:
                            print("Parsing Error: invalid expression")
                            exit()
                stmt_ident.exprs = exprs
                if self._peek() == TokenType.R_PAREN:
                    self._consume()
                else:
                    print("Parsing Error: missing ')'")
                    exit()
            else:
                print("Parsing Error: unexpected identifier")
                exit()
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
        while self._peek() is not None:
            if self._peek() == TokenType.NEW_LINE:
                self._consume()
                continue
            stmt = self._parseStmt()
            if stmt is not None:
                prog.stmts.append(stmt)
            else:
                print("Parsing Error: invalid statement")
                exit()
        return prog

    def parse(self) -> NodeProg:
        return self._parseProg()
