from modules.parse.nodes import *
from modules.generate.classes import *
from modules.generate.common import *


class Generator:
    def __init__(self, prog: NodeProg):
        GenVars.prog = prog

    def generate(self) -> str:
        output = ""
        GenCalls.genProg()
        for line in GenVars.output:
            output += line
        return output
