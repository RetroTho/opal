from enum import Enum, auto
from modules.parse.nodes import *
from modules.generate.classes import *
from modules.generate.common import *


class Generator:
    def __init__(self, prog: NodeProg):
        GenVars.prog = prog

    def _genTerm(self, term: NodeTerm):
        if isinstance(term.vari, NodeTermIntLit):
            term_int_lit = term.vari
            GenVars.buffer += term_int_lit.int_lit.value
            GenVars.last_data_type = DataType.INT
        elif isinstance(term.vari, NodeTermStrLit):
            term_str_lit = term.vari
            GenVars.buffer += '"' + term_str_lit.str_lit.value + '"'
            GenVars.last_data_type = DataType.STR
        elif isinstance(term.vari, NodeTermVar):
            term_ident = term.vari
            index = None
            for i in range(len(GenVars.variables)):
                if GenVars.variables[i].name == term_ident.ident.value:
                    index = i
            if index is None:
                print("Generating Error: undeclared variable")
                exit()
            GenVars.buffer += term_ident.ident.value
            GenVars.last_data_type = GenVars.variables[index].type
        elif isinstance(term.vari, NodeTermFuncCall):
            term_func_call = term.vari
            index = None
            for i in range(len(GenVars.functions)):
                if GenVars.functions[i].name == term_func_call.ident.value:
                    index = i
            if index is None:
                print("Generating Error: undeclared function")
                exit()
            GenVars.buffer += term_func_call.ident.value + "("
            if len(term_func_call.exprs) != len(GenVars.functions[index].args):
                print(
                    "Generating Error: incorrect number of arguments in function call"
                )
                exit()
            for i in range(len(term_func_call.exprs)):
                self._genExpr(term_func_call.exprs[i])
                if GenVars.last_data_type != GenVars.functions[index].args[i].type:
                    print("Generating Error: incorrect argument data type")
                    exit()
                if i != len(term_func_call.exprs) - 1:
                    GenVars.buffer += ","
            GenVars.buffer += ")"
            GenVars.last_data_type = GenVars.functions[index].return_type

        elif isinstance(term.vari, NodeTermParen):
            term_paren = term.vari
            GenVars.buffer += "("
            self._genExpr(term_paren.expr)
            GenVars.buffer += ")"

    def _genBinaryExpr(self, binary_expr: NodeBinaryExpr):
        if isinstance(binary_expr.vari, NodeBinaryExprIsEq):
            is_eq = binary_expr.vari
            self._genExpr(is_eq.left)
            GenVars.buffer += "=="
            self._genExpr(is_eq.right)
        elif isinstance(binary_expr.vari, NodeBinaryExprAdd):
            add = binary_expr.vari
            self._genExpr(add.left)
            GenVars.buffer += "+"
            self._genExpr(add.right)
        elif isinstance(binary_expr.vari, NodeBinaryExprSub):
            sub = binary_expr.vari
            self._genExpr(sub.left)
            GenVars.buffer += "-"
            self._genExpr(sub.right)
        elif isinstance(binary_expr.vari, NodeBinaryExprMult):
            mult = binary_expr.vari
            self._genExpr(mult.left)
            GenVars.buffer += "*"
            self._genExpr(mult.right)
        elif isinstance(binary_expr.vari, NodeBinaryExprDiv):
            div = binary_expr.vari
            self._genExpr(div.left)
            GenVars.buffer += "/"
            self._genExpr(div.right)

    def _genExpr(self, expr: NodeExpr):
        if isinstance(expr.vari, NodeTerm):
            term = expr.vari
            self._genTerm(term)
        elif isinstance(expr.vari, NodeBinaryExpr):
            binary_expr = expr.vari
            self._genBinaryExpr(binary_expr)

    def _genScope(self, scope: NodeScope):
        GenVars.in_scope = True
        vars_length = len(GenVars.variables)
        GenVars.output.append("{\n")
        for stmt in scope.stmts:
            self._genStmt(stmt)
        GenVars.output.append("}\n")
        scope_vars = []
        for i in range(len(GenVars.variables) - vars_length):
            scope_vars.append(GenVars.variables[-1])
            del GenVars.variables[-1]
        GenVars.scope_variables.append(scope_vars)
        GenVars.in_scope = False

    def _genStmt(self, stmt: NodeStmt):
        GenVars.buffer = ""
        if isinstance(stmt.vari, NodeStmtExit):
            stmt_exit = stmt.vari
            GenVars.buffer += "exit("
            self._genExpr(stmt_exit.expr)
            GenVars.buffer += ");\n"
            GenVars.output.append(GenVars.buffer)
        elif isinstance(stmt.vari, NodeStmtReturn):
            stmt_return = stmt.vari
            GenVars.buffer += "return("
            self._genExpr(stmt_return.expr)
            GenVars.buffer += ");\n"
            if GenVars.last_func_data_type == GenVars.last_data_type:
                GenVars.output.append(GenVars.buffer)
            else:
                print("Generating Error: incorrect return type")
                exit()
        elif isinstance(stmt.vari, NodeStmtPrint):
            stmt_print = stmt.vari
            self._genExpr(stmt_print.expr)
            if GenVars.last_data_type == DataType.INT:
                GenVars.buffer = 'printf("%d\\n",' + GenVars.buffer + ");\n"
            elif GenVars.last_data_type == DataType.STR:
                GenVars.buffer = 'printf("%s\\n",' + GenVars.buffer + ");\n"
            GenVars.output.append(GenVars.buffer)
        elif isinstance(stmt.vari, NodeStmtIf):
            stmt_if = stmt.vari
            GenVars.buffer += "if("
            self._genExpr(stmt_if.expr)
            GenVars.buffer += ")"
            GenVars.output.append(GenVars.buffer)
            self._genScope(stmt_if.scope)
        elif isinstance(stmt.vari, NodeStmtWhile):
            stmt_while = stmt.vari
            GenVars.buffer += "while("
            self._genExpr(stmt_while.expr)
            GenVars.buffer += ")"
            GenVars.output.append(GenVars.buffer)
            self._genScope(stmt_while.scope)
        elif isinstance(stmt.vari, NodeStmtVariable):
            stmt_variable = stmt.vari
            undeclared = True
            for i in range(len(GenVars.variables)):
                if GenVars.variables[i].name == stmt_variable.ident.value:
                    undeclared = False
            if not GenVars.in_scope:
                for scope in GenVars.scope_variables:
                    for i in range(len(scope)):
                        if scope[i].name == stmt_variable.ident.value:
                            undeclared = False
            if not undeclared:
                print("Generating Error: identifier already declared")
                exit()
            if stmt_variable.data_type.value == "int":
                GenVars.variables.append(
                    Variable(stmt_variable.ident.value, DataType.INT)
                )
                GenVars.buffer += "int "
                GenVars.buffer += stmt_variable.ident.value
            elif stmt_variable.data_type.value == "str":
                GenVars.variables.append(
                    Variable(stmt_variable.ident.value, DataType.STR)
                )
                GenVars.buffer += "char "
                GenVars.buffer += stmt_variable.ident.value + "[250]"
            if stmt_variable.expr is not None:
                GenVars.buffer += "="
                self._genExpr(stmt_variable.expr)
            GenVars.buffer += ";\n"
            if GenVars.in_scope:
                GenVars.output.append(GenVars.buffer)
            else:
                GenVars.output.insert(GenVars.global_index, GenVars.buffer)
                GenVars.global_index += 1
        elif isinstance(stmt.vari, NodeStmtFunction):
            stmt_function = stmt.vari
            line_count = len(GenVars.output)
            var_count = len(GenVars.variables)
            undeclared = True
            for i in range(len(GenVars.functions)):
                if GenVars.functions[i].name == stmt_function.ident.value:
                    undeclared = False
            if not undeclared:
                print("Generating Error: function already declared")
                exit()
            returns = None
            args = []
            if stmt_function.returns is not None:
                if stmt_function.returns.vari.data_type.value == "int":
                    returns = DataType.INT
                    GenVars.last_func_data_type = DataType.INT
                    GenVars.buffer += "int "
                elif stmt_function.returns.vari.data_type.value == "str":
                    returns = DataType.STR
                    GenVars.last_func_data_type = DataType.STR
                    GenVars.buffer += "char* "
            else:
                GenVars.buffer += "void "
            GenVars.buffer += stmt_function.ident.value + "("
            if stmt_function.takes is not None:
                for i in range(len(stmt_function.takes)):
                    if i != 0:
                        GenVars.buffer += ","
                    takes_ident = stmt_function.takes[i].vari.ident.value
                    takes_data_type = None
                    if stmt_function.takes[i].vari.data_type.value == "int":
                        takes_data_type = DataType.INT
                        GenVars.buffer += "int " + takes_ident
                    elif stmt_function.takes[i].vari.data_type.value == "str":
                        takes_data_type = DataType.STR
                        GenVars.buffer += "char* " + takes_ident
                    args.append(Variable(takes_ident, takes_data_type))
                    GenVars.variables.append(Variable(takes_ident, takes_data_type))
            GenVars.functions.append(Function(stmt_function.ident.value, returns, args))
            GenVars.buffer += ")"
            GenVars.output.append(GenVars.buffer)
            self._genScope(stmt_function.scope)
            for i in range(len(GenVars.output) - line_count):
                GenVars.output.insert(GenVars.global_index, GenVars.output[-1])
                del GenVars.output[-1]
            for i in range(len(GenVars.variables) - var_count):
                del GenVars.variables[-1]
            GenVars.global_index += len(GenVars.output) - line_count
        elif isinstance(stmt.vari, NodeStmtFuncCall):
            stmt_func_call = stmt.vari
            index = None
            for i in range(len(GenVars.functions)):
                if GenVars.functions[i].name == stmt_func_call.ident.value:
                    index = i
            if index is None:
                print("Generating Error: undeclared function")
                exit()
            GenVars.buffer += stmt_func_call.ident.value + "("
            if len(stmt_func_call.exprs) != len(GenVars.functions[index].args):
                print(
                    "Generating Error: incorrect number of arguments in function call"
                )
                exit()
            for i in range(len(stmt_func_call.exprs)):
                self._genExpr(stmt_func_call.exprs[i])
                if GenVars.last_data_type != GenVars.functions[index].args[i].type:
                    print("Generating Error: incorrect argument data type")
                    exit()
                if i != len(stmt_func_call.exprs) - 1:
                    GenVars.buffer += ","
            GenVars.buffer += ");\n"
            GenVars.output.append(GenVars.buffer)
        elif isinstance(stmt.vari, NodeStmtVarAssign):
            stmt_ident = stmt.vari
            undeclared = True
            for i in range(len(GenVars.variables)):
                if GenVars.variables[i].name == stmt_ident.ident.value:
                    undeclared = False
            if undeclared:
                print("Generating Error: undeclared variable")
                exit()
            GenVars.buffer += stmt_ident.ident.value + "="
            self._genExpr(stmt_ident.expr)
            GenVars.buffer += ";\n"
            GenVars.output.append(GenVars.buffer)

    def _genProg(self):
        GenVars.output.append("#include <stdlib.h>\n")
        GenVars.output.append("#include <stdio.h>\n")
        GenVars.output.append("int main(){\n")
        for stmt in GenVars.prog.stmts:
            self._genStmt(stmt)
        GenVars.output.append("return 0;}")

    def generate(self) -> str:
        output = ""
        self._genProg()
        for line in GenVars.output:
            output += line
        return output
