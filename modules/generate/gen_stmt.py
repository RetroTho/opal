from modules.generate.classes import *
from modules.generate.common import *


class GenStmt:
    def generate(self, stmt: NodeStmt):
        GenVars.buffer = ""
        if isinstance(stmt.vari, NodeStmtExit):
            stmt_exit = stmt.vari
            GenVars.buffer += "exit("
            GenCalls.genExpr(stmt_exit.expr)
            GenVars.buffer += ");\n"
            GenVars.output.append(GenVars.buffer)
        elif isinstance(stmt.vari, NodeStmtReturn):
            stmt_return = stmt.vari
            GenVars.buffer += "return("
            GenCalls.genExpr(stmt_return.expr)
            GenVars.buffer += ");\n"
            if GenVars.last_func_data_type == GenVars.last_data_type:
                GenVars.output.append(GenVars.buffer)
            else:
                print("Generating Error: incorrect return type")
                exit()
        elif isinstance(stmt.vari, NodeStmtPrint):
            stmt_print = stmt.vari
            GenCalls.genExpr(stmt_print.expr)
            if GenVars.last_data_type == DataType.INT:
                GenVars.buffer = 'printf("%d\\n",' + GenVars.buffer + ");\n"
            elif GenVars.last_data_type == DataType.STR:
                GenVars.buffer = 'printf("%s\\n",' + GenVars.buffer + ");\n"
            GenVars.output.append(GenVars.buffer)
        elif isinstance(stmt.vari, NodeStmtIf):
            stmt_if = stmt.vari
            GenVars.buffer += "if("
            GenCalls.genExpr(stmt_if.expr)
            GenVars.buffer += ")"
            GenVars.output.append(GenVars.buffer)
            GenCalls.genScope(stmt_if.scope)
        elif isinstance(stmt.vari, NodeStmtWhile):
            stmt_while = stmt.vari
            GenVars.buffer += "while("
            GenCalls.genExpr(stmt_while.expr)
            GenVars.buffer += ")"
            GenVars.output.append(GenVars.buffer)
            GenCalls.genScope(stmt_while.scope)
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
                GenCalls.genExpr(stmt_variable.expr)
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
            GenCalls.genScope(stmt_function.scope)
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
                GenCalls.genExpr(stmt_func_call.exprs[i])
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
            GenCalls.genExpr(stmt_ident.expr)
            GenVars.buffer += ";\n"
            GenVars.output.append(GenVars.buffer)
