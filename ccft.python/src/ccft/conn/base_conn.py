from multiprocessing import Queue

from ccft.cmd.instruction_converter import InstructionConverter
from ccft.conn.conn_token import Token


class AbstConn:
    _Queue: Queue
    _Token: Token
    _Converter: InstructionConverter

    def __init__(self, queue: Queue, token: Token, converter: InstructionConverter):
        self._Queue = queue
        self._Token = token
        self._Converter = converter

    def start(self) -> bool:
        pass

    def start_recv(self):
        pass

    def send(self, message: str):
        pass

    def reply(self, cmd_id: int, status: bool, message: str = None, **kwargs):
        pass

    def close(self):
        pass

    def is_connected(self):
        return self._Token.Status()
        pass

    def send_heartbeat(self, count: str):
        pass
