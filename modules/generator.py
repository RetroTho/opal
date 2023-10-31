from enum import Enum, auto
from modules.parser import *


class DataType(Enum):
    INT = auto()
    STR = auto()


class Generator:
    _variables = []
    _last_data_type = None
    _buffer = ""
    _output = []

    def __init__(self, prog: NodeProg):
        self._prog = prog

    def _genTerm(self, term: NodeTerm):
        if isinstance(term.vari, NodeTermIntLit):
            term_int_lit = term.vari
            self._buffer += term_int_lit.int_lit.value
            self._last_data_type = DataType.INT
        elif isinstance(term.vari, NodeTermStrLit):
            term_str_lit = term.vari
            self._buffer += '"' + term_str_lit.str_lit.value + '"'
            self._last_data_type = DataType.STR
        elif isinstance(term.vari, NodeTermParen):
            term_paren = term.vari
            self._buffer += "("
            self._genExpr(term_paren.expr)
            self._buffer += ")"

    def _genExpr(self, expr: NodeExpr):
        if isinstance(expr.vari, NodeTerm):
            term = expr.vari
            self._genTerm(term)

    def _genStmt(self, stmt: NodeStmt):
        self._buffer = ""
        if isinstance(stmt.vari, NodeStmtExit):
            stmt_exit = stmt.vari
            self._buffer += "exit("
            self._genExpr(stmt_exit.expr)
            self._buffer += ");\n"
            self._output.append(self._buffer)
        elif isinstance(stmt.vari, NodeStmtPrint):
            stmt_print = stmt.vari
            self._genExpr(stmt_print.expr)
            if self._last_data_type == DataType.INT:
                self._buffer = 'printf("%d\\n",' + self._buffer + ");\n"
            elif self._last_data_type == DataType.STR:
                self._buffer = 'printf("%s\\n",' + self._buffer + ");\n"
            self._output.append(self._buffer)
        elif isinstance(stmt.vari, NodeStmtVariable):
            stmt_variable = stmt.vari
            if stmt_variable.ident.value in self._variables:
                print("Generating Error: identifier already declared")
                exit()
            else:
                self._variables.append(stmt_variable.ident.value)
            if stmt_variable.data_type.value == "int":
                self._buffer += "int "
                self._buffer += stmt_variable.ident.value
            elif stmt_variable.data_type.value == "str":
                self._buffer += "char "
                self._buffer += stmt_variable.ident.value + "[250]"
            if stmt_variable.expr is not None:
                self._buffer += "="
                self._genExpr(stmt_variable.expr)
            self._buffer += ";\n"
            self._output.append(self._buffer)
        elif isinstance(stmt.vari, NodeStmtIdent):
            stmt_ident = stmt.vari
            if not stmt_ident.ident.value in self._variables:
                print("Generating Error: undeclared identifier")
                exit()
            self._buffer += stmt_ident.ident.value + "="
            self._genExpr(stmt_ident.expr)
            self._buffer += ";\n"
            self._output.append(self._buffer)

    def _genProg(self):
        self._output.append("#include <stdlib.h>\n")
        self._output.append("#include <stdio.h>\n")
        self._output.append("int main(){\n")
        for stmt in self._prog.stmts:
            self._genStmt(stmt)
        self._output.append("return 0;}")

    def generate(self) -> str:
        output = ""
        self._genProg()
        for line in self._output:
            output += line
        return output
