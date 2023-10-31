from enum import Enum, auto
from modules.parser import *


class DataType(Enum):
    INT = auto()
    STR = auto()


@dataclass
class Variable:
    name: str
    type: DataType


class Generator:
    _variables: list[Variable] = []
    _last_data_type: DataType = None
    _buffer: str = ""
    _output: list[str] = []

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
        elif isinstance(term.vari, NodeTermIdent):
            term_ident = term.vari
            index = None
            for i in range(len(self._variables)):
                if self._variables[i].name == term_ident.ident.value:
                    index = i
            if index is None:
                print("Generating Error: undeclared identifier")
                exit()
            self._buffer += term_ident.ident.value
            self._last_data_type = self._variables[index].type
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
            undeclared = True
            for i in range(len(self._variables)):
                if self._variables[i].name == stmt_variable.ident.value:
                    undeclared = False
            if not undeclared:
                print("Generating Error: identifier already declared")
                exit()
            if stmt_variable.data_type.value == "int":
                self._variables.append(
                    Variable(stmt_variable.ident.value, DataType.INT)
                )
                self._buffer += "int "
                self._buffer += stmt_variable.ident.value
            elif stmt_variable.data_type.value == "str":
                self._variables.append(
                    Variable(stmt_variable.ident.value, DataType.STR)
                )
                self._buffer += "char "
                self._buffer += stmt_variable.ident.value + "[250]"
            if stmt_variable.expr is not None:
                self._buffer += "="
                self._genExpr(stmt_variable.expr)
            self._buffer += ";\n"
            self._output.append(self._buffer)
        elif isinstance(stmt.vari, NodeStmtIdent):
            stmt_ident = stmt.vari
            undeclared = True
            for i in range(len(self._variables)):
                if self._variables[i].name == stmt_ident.ident.value:
                    undeclared = False
            if undeclared:
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
