from modules.parse.nodes import *
from modules.generate.classes import *

class GenVars:
    prog: NodeProg = None
    variables: list[Variable] = []
    scope_variables: list[list[Variable]] = []
    functions: list[Function] = []
    last_data_type: DataType = None
    last_func_data_type: DataType = None
    global_index: int = 2
    in_scope: bool = False
    buffer: str = ""
    output: list[str] = []