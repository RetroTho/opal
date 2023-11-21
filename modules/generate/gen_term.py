from modules.generate.classes import *
from modules.generate.common import *


class GenTerm:
    def generate(self, term: NodeTerm):
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
                GenCalls.genExpr(term_func_call.exprs[i])
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
            GenCalls.genExpr(term_paren.expr)
            GenVars.buffer += ")"
