from enum import Enum, auto
from modules.parser import *
from modules.generate.classes import *


class Generator:
    def __init__(self, prog: NodeProg):
        self._prog = prog
        self._variables: list[Variable] = []
        self._scope_variables: list[list[Variable]] = []
        self._functions: list[Function] = []
        self._last_data_type: DataType = None
        self._last_func_data_type: DataType = None
        self._global_index: int = 2
        self._in_scope: bool = False
        self._buffer: str = ""
        self._output: list[str] = []

    def _genTerm(self, term: NodeTerm):
        if isinstance(term.vari, NodeTermIntLit):
            term_int_lit = term.vari
            self._buffer += term_int_lit.int_lit.value
            self._last_data_type = DataType.INT
        elif isinstance(term.vari, NodeTermStrLit):
            term_str_lit = term.vari
            self._buffer += '"' + term_str_lit.str_lit.value + '"'
            self._last_data_type = DataType.STR
        elif isinstance(term.vari, NodeTermVar):
            term_ident = term.vari
            index = None
            for i in range(len(self._variables)):
                if self._variables[i].name == term_ident.ident.value:
                    index = i
            if index is None:
                print("Generating Error: undeclared variable")
                exit()
            self._buffer += term_ident.ident.value
            self._last_data_type = self._variables[index].type
        elif isinstance(term.vari, NodeTermFuncCall):
            term_func_call = term.vari
            index = None
            for i in range(len(self._functions)):
                if self._functions[i].name == term_func_call.ident.value:
                    index = i
            if index is None:
                print("Generating Error: undeclared function")
                exit()
            self._buffer += term_func_call.ident.value + "("
            if len(term_func_call.exprs) != len(self._functions[index].args):
                print(
                    "Generating Error: incorrect number of arguments in function call"
                )
                exit()
            for i in range(len(term_func_call.exprs)):
                self._genExpr(term_func_call.exprs[i])
                if self._last_data_type != self._functions[index].args[i].type:
                    print("Generating Error: incorrect argument data type")
                    exit()
                if i != len(term_func_call.exprs) - 1:
                    self._buffer += ","
            self._buffer += ")"
            self._last_data_type = self._functions[index].return_type

        elif isinstance(term.vari, NodeTermParen):
            term_paren = term.vari
            self._buffer += "("
            self._genExpr(term_paren.expr)
            self._buffer += ")"

    def _genBinaryExpr(self, binary_expr: NodeBinaryExpr):
        if isinstance(binary_expr.vari, NodeBinaryExprIsEq):
            is_eq = binary_expr.vari
            self._genExpr(is_eq.left)
            self._buffer += "=="
            self._genExpr(is_eq.right)
        elif isinstance(binary_expr.vari, NodeBinaryExprAdd):
            add = binary_expr.vari
            self._genExpr(add.left)
            self._buffer += "+"
            self._genExpr(add.right)
        elif isinstance(binary_expr.vari, NodeBinaryExprSub):
            sub = binary_expr.vari
            self._genExpr(sub.left)
            self._buffer += "-"
            self._genExpr(sub.right)
        elif isinstance(binary_expr.vari, NodeBinaryExprMult):
            mult = binary_expr.vari
            self._genExpr(mult.left)
            self._buffer += "*"
            self._genExpr(mult.right)
        elif isinstance(binary_expr.vari, NodeBinaryExprDiv):
            div = binary_expr.vari
            self._genExpr(div.left)
            self._buffer += "/"
            self._genExpr(div.right)

    def _genExpr(self, expr: NodeExpr):
        if isinstance(expr.vari, NodeTerm):
            term = expr.vari
            self._genTerm(term)
        elif isinstance(expr.vari, NodeBinaryExpr):
            binary_expr = expr.vari
            self._genBinaryExpr(binary_expr)

    def _genScope(self, scope: NodeScope):
        self._in_scope = True
        vars_length = len(self._variables)
        self._output.append("{\n")
        for stmt in scope.stmts:
            self._genStmt(stmt)
        self._output.append("}\n")
        scope_vars = []
        for i in range(len(self._variables) - vars_length):
            scope_vars.append(self._variables[-1])
            del self._variables[-1]
        self._scope_variables.append(scope_vars)
        self._in_scope = False

    def _genStmt(self, stmt: NodeStmt):
        self._buffer = ""
        if isinstance(stmt.vari, NodeStmtExit):
            stmt_exit = stmt.vari
            self._buffer += "exit("
            self._genExpr(stmt_exit.expr)
            self._buffer += ");\n"
            self._output.append(self._buffer)
        elif isinstance(stmt.vari, NodeStmtReturn):
            stmt_return = stmt.vari
            self._buffer += "return("
            self._genExpr(stmt_return.expr)
            self._buffer += ");\n"
            if self._last_func_data_type == self._last_data_type:
                self._output.append(self._buffer)
            else:
                print("Generating Error: incorrect return type")
                exit()
        elif isinstance(stmt.vari, NodeStmtPrint):
            stmt_print = stmt.vari
            self._genExpr(stmt_print.expr)
            if self._last_data_type == DataType.INT:
                self._buffer = 'printf("%d\\n",' + self._buffer + ");\n"
            elif self._last_data_type == DataType.STR:
                self._buffer = 'printf("%s\\n",' + self._buffer + ");\n"
            self._output.append(self._buffer)
        elif isinstance(stmt.vari, NodeStmtIf):
            stmt_if = stmt.vari
            self._buffer += "if("
            self._genExpr(stmt_if.expr)
            self._buffer += ")"
            self._output.append(self._buffer)
            self._genScope(stmt_if.scope)
        elif isinstance(stmt.vari, NodeStmtWhile):
            stmt_while = stmt.vari
            self._buffer += "while("
            self._genExpr(stmt_while.expr)
            self._buffer += ")"
            self._output.append(self._buffer)
            self._genScope(stmt_while.scope)
        elif isinstance(stmt.vari, NodeStmtVariable):
            stmt_variable = stmt.vari
            undeclared = True
            for i in range(len(self._variables)):
                if self._variables[i].name == stmt_variable.ident.value:
                    undeclared = False
            if not self._in_scope:
                for scope in self._scope_variables:
                    for i in range(len(scope)):
                        if scope[i].name == stmt_variable.ident.value:
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
            if self._in_scope:
                self._output.append(self._buffer)
            else:
                self._output.insert(self._global_index, self._buffer)
                self._global_index += 1
        elif isinstance(stmt.vari, NodeStmtFunction):
            stmt_function = stmt.vari
            line_count = len(self._output)
            var_count = len(self._variables)
            undeclared = True
            for i in range(len(self._functions)):
                if self._functions[i].name == stmt_function.ident.value:
                    undeclared = False
            if not undeclared:
                print("Generating Error: function already declared")
                exit()
            returns = None
            args = []
            if stmt_function.returns is not None:
                if stmt_function.returns.vari.data_type.value == "int":
                    returns = DataType.INT
                    self._last_func_data_type = DataType.INT
                    self._buffer += "int "
                elif stmt_function.returns.vari.data_type.value == "str":
                    returns = DataType.STR
                    self._last_func_data_type = DataType.STR
                    self._buffer += "char* "
            else:
                self._buffer += "void "
            self._buffer += stmt_function.ident.value + "("
            if stmt_function.takes is not None:
                for i in range(len(stmt_function.takes)):
                    if i != 0:
                        self._buffer += ","
                    takes_ident = stmt_function.takes[i].vari.ident.value
                    takes_data_type = None
                    if stmt_function.takes[i].vari.data_type.value == "int":
                        takes_data_type = DataType.INT
                        self._buffer += "int " + takes_ident
                    elif stmt_function.takes[i].vari.data_type.value == "str":
                        takes_data_type = DataType.STR
                        self._buffer += "char* " + takes_ident
                    args.append(Variable(takes_ident, takes_data_type))
                    self._variables.append(Variable(takes_ident, takes_data_type))
            self._functions.append(Function(stmt_function.ident.value, returns, args))
            self._buffer += ")"
            self._output.append(self._buffer)
            self._genScope(stmt_function.scope)
            for i in range(len(self._output) - line_count):
                self._output.insert(self._global_index, self._output[-1])
                del self._output[-1]
            for i in range(len(self._variables) - var_count):
                del self._variables[-1]
            self._global_index += len(self._output) - line_count
        elif isinstance(stmt.vari, NodeStmtFuncCall):
            stmt_func_call = stmt.vari
            index = None
            for i in range(len(self._functions)):
                if self._functions[i].name == stmt_func_call.ident.value:
                    index = i
            if index is None:
                print("Generating Error: undeclared function")
                exit()
            self._buffer += stmt_func_call.ident.value + "("
            if len(stmt_func_call.exprs) != len(self._functions[index].args):
                print(
                    "Generating Error: incorrect number of arguments in function call"
                )
                exit()
            for i in range(len(stmt_func_call.exprs)):
                self._genExpr(stmt_func_call.exprs[i])
                if self._last_data_type != self._functions[index].args[i].type:
                    print("Generating Error: incorrect argument data type")
                    exit()
                if i != len(stmt_func_call.exprs) - 1:
                    self._buffer += ","
            self._buffer += ");\n"
            self._output.append(self._buffer)
        elif isinstance(stmt.vari, NodeStmtVarAssign):
            stmt_ident = stmt.vari
            undeclared = True
            for i in range(len(self._variables)):
                if self._variables[i].name == stmt_ident.ident.value:
                    undeclared = False
            if undeclared:
                print("Generating Error: undeclared variable")
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
