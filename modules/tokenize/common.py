class TokFuncs:
    def peek(offset: int = 0) -> str:
        if TokVars.index + offset < len(TokVars.src):
            return TokVars.src[TokVars.index + offset]
        else:
            return None

    def consume() -> str:
        TokVars.index += 1
        return TokVars.src[TokVars.index - 1]


class TokVars:
    src: str = None
    index: int = 0
