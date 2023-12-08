from modules.parse.nodes import *
from modules.generate.classes import *
from modules.generate.common import *


class Generator:
    def __init__(self, prog: NodeProg):
        GenVars.prog = prog

    def generate(self) -> str:
        output_str = ""
        GenCalls.genProg()
        for line in GenVars.output:
            output_str += line
        return output_str
