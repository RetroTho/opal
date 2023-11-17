from modules.tokenize.tokens import *
from modules.parse.nodes import *
from modules.parse.common import *


class Parser:
    def __init__(self, tokens: list[Token]):
        ParseVars.tokens = tokens

    def parse(self) -> NodeProg:
        return ParseCalls.parseProg()
