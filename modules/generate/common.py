from modules.parse.nodes import *
from modules.generate.classes import *


class GenCalls:
    def genTerm(term: NodeTerm):
        from modules.generate.gen_term import GenTerm

        GenTerm().generate(term)

    def genBinExpr(binary_expr: NodeBinaryExpr):
        from modules.generate.gen_bin_expr import GenBinExpr

        GenBinExpr().generate(binary_expr)

    def genExpr(expr: NodeExpr):
        from modules.generate.gen_expr import GenExpr

        GenExpr().generate(expr)

    def genScope(scope: NodeScope):
        from modules.generate.gen_scope import GenScope

        GenScope().generate(scope)

    def genStmt(stmt: NodeStmt):
        from modules.generate.gen_stmt import GenStmt

        GenStmt().generate(stmt)

    def genProg():
        from modules.generate.gen_prog import GenProg

        GenProg().generate()


class GenVars:
    prog: NodeProg = None
    variables: list[Variable] = []
    scope_variables: list[list[Variable]] = []
    functions: list[Function] = []
    last_data_type: DataType = None
    last_func_data_type: DataType = None
    global_index: int = 2
    in_scope: bool = False
    buffer: str = ""
    output: list[str] = []
