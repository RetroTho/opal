from modules.generate.classes import *
from modules.generate.common import *


class GenBinExpr:
    def _matchBinExpr(
        self,
        vari: (
            NodeBinaryExprIsEq
            | NodeBinaryExprAdd
            | NodeBinaryExprSub
            | NodeBinaryExprMult
            | NodeBinaryExprDiv
        ),
    ) -> str:
        match vari:
            case NodeBinaryExprIsEq():
                return "=="
            case NodeBinaryExprAdd():
                return "+"
            case NodeBinaryExprSub():
                return "-"
            case NodeBinaryExprMult():
                return "*"
            case NodeBinaryExprDiv():
                return "/"
            case _:
                print("Generating Error: invalid binary operation")
                exit()

    def generate(self, binary_expr: NodeBinaryExpr):
        bin_expr_vari = binary_expr.vari
        GenCalls.genExpr(bin_expr_vari.left)
        GenVars.buffer += self._matchBinExpr(bin_expr_vari)
        GenCalls.genExpr(bin_expr_vari.right)
