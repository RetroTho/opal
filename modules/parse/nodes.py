from __future__ import annotations
from dataclasses import dataclass
from modules.tokenizer import Token


@dataclass
class NodeTermIntLit:
    int_lit: Token = None  # INT_LIT


@dataclass
class NodeTermStrLit:
    str_lit: Token = None  # STR_LIT


@dataclass
class NodeTermVar:
    ident: Token = None  # IDENT


@dataclass
class NodeTermFuncCall:
    ident: Token = None  # IDENT
    exprs: list[NodeExpr] = None


@dataclass
class NodeTermParen:
    expr: NodeExpr = None


@dataclass
class NodeTerm:
    vari: (
        NodeTermIntLit | NodeTermStrLit | NodeTermVar | NodeTermFuncCall | NodeTermParen
    ) = None


@dataclass
class NodeBinaryExprIsEq:
    left: NodeExpr = None
    right: NodeExpr = None


@dataclass
class NodeBinaryExprAdd:
    left: NodeExpr = None
    right: NodeExpr = None


@dataclass
class NodeBinaryExprSub:
    left: NodeExpr = None
    right: NodeExpr = None


@dataclass
class NodeBinaryExprMult:
    left: NodeExpr = None
    right: NodeExpr = None


@dataclass
class NodeBinaryExprDiv:
    left: NodeExpr = None
    right: NodeExpr = None


@dataclass
class NodeBinaryExpr:
    vari: (
        NodeBinaryExprIsEq
        | NodeBinaryExprAdd
        | NodeBinaryExprSub
        | NodeBinaryExprMult
        | NodeBinaryExprDiv
    ) = None


@dataclass
class NodeExpr:
    vari: (NodeTerm | NodeBinaryExpr) = None


@dataclass
class NodeDetailReturns:
    data_type: Token = None  # DATA_TYPE


@dataclass
class NodeDetailTakes:
    data_type: Token = None  # DATA_TYPE
    ident: Token = None  # IDENT


@dataclass
class NodeDetail:
    vari: (NodeDetailReturns | NodeDetailTakes) = None


@dataclass
class NodeStmtExit:
    expr: NodeExpr = None


@dataclass
class NodeStmtReturn:
    expr: NodeExpr = None


@dataclass
class NodeStmtPrint:
    expr: NodeExpr = None


@dataclass
class NodeStmtIf:
    expr: NodeExpr = None
    scope: NodeScope = None


@dataclass
class NodeStmtWhile:
    expr: NodeExpr = None
    scope: NodeScope = None


@dataclass
class NodeStmtVariable:
    ident: Token = None  # IDENT
    data_type: Token = None  # DATA_TYPE
    expr: NodeExpr = None


@dataclass
class NodeStmtFunction:
    ident: Token = None  # IDENT
    takes: list[NodeDetail] = None
    returns: NodeDetail = None
    scope: NodeScope = None


@dataclass
class NodeStmtFuncCall:
    ident: Token = None  # IDENT
    exprs: list[NodeExpr] = None


@dataclass
class NodeStmtVarAssign:
    ident: Token = None  # IDENT
    expr: NodeExpr = None


@dataclass
class NodeStmt:
    vari: (
        NodeStmtExit
        | NodeStmtReturn
        | NodeStmtPrint
        | NodeStmtIf
        | NodeStmtWhile
        | NodeStmtVariable
        | NodeStmtFunction
        | NodeStmtFuncCall
        | NodeStmtVarAssign
    ) = None


@dataclass
class NodeScope:
    stmts: list[NodeStmt] = None


@dataclass
class NodeProg:
    stmts: list[NodeStmt] = None
