from enum import Enum


class ErrorCode(Enum):
    File_NotFound = 1,
    Dir_NotFound = 2,

    Command_NotFound = 11,
    Command_NotKnow = 12,
    Command_Error = 13,

    Parameter_Error = 21,

    Object_NotFound = 31,

    IO_Error = 41,
