from modules.generate.classes import *
from modules.generate.common import *


class GenExpr:
    def generate(self, expr: NodeExpr):
        if isinstance(expr.vari, NodeTerm):
            term = expr.vari
            GenCalls.genTerm(term)
        elif isinstance(expr.vari, NodeBinaryExpr):
            binary_expr = expr.vari
            GenCalls.genBinExpr(binary_expr)
