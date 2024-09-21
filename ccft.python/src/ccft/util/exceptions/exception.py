from ccft.util.exceptions.error_code import ErrorCode


class CustomException(Exception):
    def __init__(self, code: ErrorCode, message: str, source: str = ""):
        self.__code: ErrorCode = code
        self.__source: str = source
        self.__message: str = message

    def get_code(self) -> ErrorCode:
        return self.__code

    def get_message(self) -> str:
        return self.__message

    def get_source(self) -> str:
        return self.__source

    def __str__(self):
        if self.__source == "":
            return f"error code: {self.__code.name}, {self.__message}"
        else:
            return f"error code: {self.__code.name}, {self.__source} -> {self.__message}"

    def __repr__(self):
        return self.__str__()
