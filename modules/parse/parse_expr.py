from modules.tokenizer import TokenType
from modules.parse.nodes import *
from modules.parse.common import *


class ParseExpr:
    def _matchOp(self, op: Token):
        match op.type:
            case TokenType.EQ_EQ:
                return NodeBinaryExprIsEq()
            case TokenType.PLUS:
                return NodeBinaryExprAdd()
            case TokenType.MINUS:
                return NodeBinaryExprSub()
            case TokenType.STAR:
                return NodeBinaryExprMult()
            case TokenType.F_SLASH:
                return NodeBinaryExprDiv()
            case _:
                print("Parsing Error: invalid binary operator")
                exit()

    def parse(self, min_prece: int = 0) -> NodeExpr:
        term_left = ParseCalls.parseTerm()
        if term_left is None:
            return None
        expr = NodeExpr()
        expr.vari = term_left
        while True:
            curr_token_type = ParseFuncs.peek()
            if curr_token_type is not None:
                prece = ParseFuncs.binaryPrece(curr_token_type)
                if (prece is None) or (prece < min_prece):
                    break
            else:
                break
            op = ParseFuncs.consume()
            next_min_prece = prece + 1
            expr_right = self.parse(next_min_prece)
            if expr_right is None:
                print("Parsing Error: invalid expression")
                exit()
            binary_expr = NodeBinaryExpr()
            expr_left = NodeExpr()
            expr_left.vari = expr.vari
            binary_expr_vari = self._matchOp(op)
            binary_expr_vari.left = expr_left
            binary_expr_vari.right = expr_right
            binary_expr.vari = binary_expr_vari
            expr.vari = binary_expr
        return expr
