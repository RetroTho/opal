from modules.generate.classes import *
from modules.generate.common import *


class GenProg:
    def generate(self):
        GenVars.output.append("#include <stdlib.h>\n")
        GenVars.output.append("#include <stdio.h>\n")
        GenVars.output.append("int main(){\n")
        for stmt in GenVars.prog.stmts:
            GenCalls.genStmt(stmt)
        GenVars.output.append("return 0;}")
