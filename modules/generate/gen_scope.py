from modules.generate.classes import *
from modules.generate.common import *


class GenScope:
    def generate(self, scope: NodeScope):
        GenVars.in_scope = True
        vars_length = len(GenVars.variables)
        GenVars.output.append("{\n")
        for stmt in scope.stmts:
            GenCalls.genStmt(stmt)
        GenVars.output.append("}\n")
        scope_vars = []
        for i in range(len(GenVars.variables) - vars_length):
            scope_vars.append(GenVars.variables[-1])
            del GenVars.variables[-1]
        GenVars.scope_variables.append(scope_vars)
        GenVars.in_scope = False
