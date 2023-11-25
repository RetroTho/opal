from modules.generate.classes import *
from modules.generate.common import *


class GenTerm:
    def generate(self, term: NodeTerm):
        match term.vari:
            case NodeTermIntLit():
                term_int_lit = term.vari
                GenVars.buffer += term_int_lit.int_lit.value
                GenVars.last_data_type = DataType.INT
            case NodeTermStrLit():
                term_str_lit = term.vari
                GenVars.buffer += '"' + term_str_lit.str_lit.value + '"'
                GenVars.last_data_type = DataType.STR
            case NodeTermVar():
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
            case NodeTermFuncCall():
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
                    GenCalls.genExpr(term_func_call.exprs[i])
                    if GenVars.last_data_type != GenVars.functions[index].args[i].type:
                        print("Generating Error: incorrect argument data type")
                        exit()
                    if i != len(term_func_call.exprs) - 1:
                        GenVars.buffer += ","
                GenVars.buffer += ")"
                GenVars.last_data_type = GenVars.functions[index].return_type
            case NodeTermParen():
                term_paren = term.vari
                GenVars.buffer += "("
                GenCalls.genExpr(term_paren.expr)
                GenVars.buffer += ")"
            case _:
                print("Generating Error: invalid term")
                exit()
