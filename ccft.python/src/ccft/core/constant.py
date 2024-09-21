from enum import IntEnum

EnumNone = 0x00000000


class ERelation(IntEnum):
    Nan = 0
    Contain = 1
    Call = 2
    Data = 3
    Return = 4
    Value = 4
    Control = 6


class ENode(IntEnum):
    Nan = 0
    Method = 1
    Local = 2
    Member = 3
    TypeDecl = 4
    File = 5


class EExpand(IntEnum):
    Predecessor = 1
    Successor = 2
    Dual = 3


class EEdgeWeight(IntEnum):
    Union = 1
    Sum = 2
