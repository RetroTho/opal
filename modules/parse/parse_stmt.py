from modules.tokenize.tokens import *
from modules.parse.nodes import *
from modules.parse.common import *


class ParseStmt:
    def _stmtGeneric(
        self,
        stmt_generic: (
            NodeStmtExit | NodeStmtReturn | NodeStmtPrint | NodeStmtIf | NodeStmtWhile
        ),
        hasScope: bool = False,
    ) -> NodeStmtExit | NodeStmtReturn | NodeStmtPrint | NodeStmtIf | NodeStmtWhile:
        ParseFuncs.consume()
        if ParseFuncs.peek() == TokenType.L_PAREN:
            ParseFuncs.consume()
        else:
            print("Parsing Error: missing '('")
            exit()
        expr = ParseCalls.parseExpr()
        if expr is None:
            print("Parsing Error: invalid expression")
            exit()
        stmt_generic.expr = expr
        if ParseFuncs.peek() == TokenType.R_PAREN:
            ParseFuncs.consume()
        else:
            print("Parsing Error: missing ')'")
            exit()
        if hasScope:
            stmt_generic.scope = ParseCalls.parseScope()
        if ParseFuncs.peek() == TokenType.NEW_LINE or ParseFuncs.peek() is None:
            if ParseFuncs.peek() is not None:
                ParseFuncs.consume()
        else:
            print("Parsing Error: issue ending statement")
            exit()
        return stmt_generic

    def _stmtVariable(self) -> NodeStmtVariable:
        ParseFuncs.consume()
        stmt_variable = NodeStmtVariable()
        if ParseFuncs.peek() == TokenType.IDENT:
            stmt_variable.ident = ParseFuncs.consume()
        else:
            print("Parsing Error: missing identifier")
            exit()
        if ParseFuncs.peek() == TokenType.L_PAREN:
            ParseFuncs.consume()
        else:
            print("Parsing Error: missing '('")
            exit()
        if ParseFuncs.peek() == TokenType.DATA_TYPE:
            stmt_variable.data_type = ParseFuncs.consume()
        else:
            print("Parsing Error: missing data type")
            exit()
        if ParseFuncs.peek() == TokenType.COMMA:
            ParseFuncs.consume()
            expr = ParseCalls.parseExpr()
            if expr is None:
                print("Parsing Error: invalid expression")
                exit()
            stmt_variable.expr = expr
        elif ParseFuncs.peek() != TokenType.R_PAREN:
            print("Parsing Error: missing ','")
            exit()
        if ParseFuncs.peek() == TokenType.R_PAREN:
            ParseFuncs.consume()
        else:
            print("Parsing Error: missing ')'")
            exit()
        if ParseFuncs.peek() == TokenType.NEW_LINE or ParseFuncs.peek() is None:
            if ParseFuncs.peek() is not None:
                ParseFuncs.consume()
        else:
            print("Parsing Error: issue ending statement")
            exit()
        return stmt_variable

    def _stmtFunction(self) -> NodeStmtFunction:
        ParseFuncs.consume()
        stmt_function = NodeStmtFunction()
        if ParseFuncs.peek() == TokenType.IDENT:
            stmt_function.ident = ParseFuncs.consume()
        else:
            print("Parsing Error: missing identifier")
            exit()
        if ParseFuncs.peek() == TokenType.L_PAREN:
            ParseFuncs.consume()
        else:
            print("Parsing Error: missing '('")
            exit()
        if ParseFuncs.peek() == TokenType.NEW_LINE:
            ParseFuncs.consume()
        returns = False
        first = True
        while (
            ParseFuncs.peek() == TokenType.D_RETURNS
            or ParseFuncs.peek() == TokenType.D_TAKES
            or ParseFuncs.peek() == TokenType.COMMA
        ):
            if first:
                first = False
            else:
                if ParseFuncs.peek() == TokenType.COMMA:
                    ParseFuncs.consume()
                else:
                    print("Parsing Error: missing ','")
                    exit()
                if ParseFuncs.peek() == TokenType.NEW_LINE:
                    ParseFuncs.consume()
            if ParseFuncs.peek() == TokenType.D_RETURNS:
                if not returns:
                    stmt_function.returns = ParseCalls.parseDetail()
                    returns = True
                else:
                    print("Parsing Error: return type already set")
                    exit()
            elif ParseFuncs.peek() == TokenType.D_TAKES:
                if stmt_function.takes is None:
                    stmt_function.takes = []
                stmt_function.takes.append(ParseCalls.parseDetail())
            if ParseFuncs.peek() == TokenType.NEW_LINE:
                ParseFuncs.consume()
        if ParseFuncs.peek() == TokenType.R_PAREN:
            ParseFuncs.consume()
        else:
            print("Parsing Error: missing ')'")
            exit()
        stmt_function.scope = ParseCalls.parseScope()
        if ParseFuncs.peek() == TokenType.NEW_LINE or ParseFuncs.peek() is None:
            if ParseFuncs.peek() is not None:
                ParseFuncs.consume()
        else:
            print("Parsing Error: issue ending statement")
            exit()
        return stmt_function

    def _stmtIdent(self) -> NodeStmtVarAssign | NodeStmtFuncCall:
        if ParseFuncs.peek(1) == TokenType.EQ:
            stmt_ident = NodeStmtVarAssign()
            stmt_ident.ident = ParseFuncs.consume()
            ParseFuncs.consume()
            expr = ParseCalls.parseExpr()
            if expr is None:
                print("Parsing Error: invalid expression")
                exit()
            stmt_ident.expr = expr
        elif ParseFuncs.peek(1) == TokenType.L_PAREN:
            stmt_ident = NodeStmtFuncCall()
            stmt_ident.ident = ParseFuncs.consume()
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
            stmt_ident.exprs = exprs
            if ParseFuncs.peek() == TokenType.R_PAREN:
                ParseFuncs.consume()
            else:
                print("Parsing Error: missing ')'")
                exit()
        else:
            print("Parsing Error: unexpected identifier")
            exit()
        if ParseFuncs.peek() == TokenType.NEW_LINE or ParseFuncs.peek() is None:
            if ParseFuncs.peek() is not None:
                ParseFuncs.consume()
        else:
            print("Parsing Error: issue ending statement")
            exit()
        return stmt_ident

    def parse(self) -> NodeStmt:
        stmt_vari = None
        match ParseFuncs.peek():
            case TokenType.EXIT:
                stmt_vari = self._stmtGeneric(NodeStmtExit())
            case TokenType.RETURN:
                stmt_vari = self._stmtGeneric(NodeStmtReturn())
            case TokenType.PRINT:
                stmt_vari = self._stmtGeneric(NodeStmtPrint())
            case TokenType.IF:
                stmt_vari = self._stmtGeneric(NodeStmtIf(), True)
            case TokenType.WHILE:
                stmt_vari = self._stmtGeneric(NodeStmtWhile(), True)
            case TokenType.VARIABLE:
                stmt_vari = self._stmtVariable()
            case TokenType.FUNCTION:
                stmt_vari = self._stmtFunction()
            case TokenType.IDENT:
                stmt_vari = self._stmtIdent()
            case _:
                return None
        stmt = NodeStmt()
        stmt.vari = stmt_vari
        return stmt
