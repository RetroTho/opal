from modules.generate.classes import *
from modules.generate.common import *


class GenBinExpr:
    def generate(self, binary_expr: NodeBinaryExpr):
        if isinstance(binary_expr.vari, NodeBinaryExprIsEq):
            is_eq = binary_expr.vari
            GenCalls.genExpr(is_eq.left)
            GenVars.buffer += "=="
            GenCalls.genExpr(is_eq.right)
        elif isinstance(binary_expr.vari, NodeBinaryExprAdd):
            add = binary_expr.vari
            GenCalls.genExpr(add.left)
            GenVars.buffer += "+"
            GenCalls.genExpr(add.right)
        elif isinstance(binary_expr.vari, NodeBinaryExprSub):
            sub = binary_expr.vari
            GenCalls.genExpr(sub.left)
            GenVars.buffer += "-"
            GenCalls.genExpr(sub.right)
        elif isinstance(binary_expr.vari, NodeBinaryExprMult):
            mult = binary_expr.vari
            GenCalls.genExpr(mult.left)
            GenVars.buffer += "*"
            GenCalls.genExpr(mult.right)
        elif isinstance(binary_expr.vari, NodeBinaryExprDiv):
            div = binary_expr.vari
            GenCalls.genExpr(div.left)
            GenVars.buffer += "/"
            GenCalls.genExpr(div.right)
