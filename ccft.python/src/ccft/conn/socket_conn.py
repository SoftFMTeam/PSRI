import socket
import threading
from multiprocessing import Queue

from loguru import logger

from ccft.cmd.instruction_converter import InstructionConverter
from ccft.conn.base_conn import AbstConn
from ccft.conn.conn_token import Token
from ccft.util.exceptions.exception import CustomException


class SocketConn(AbstConn):
    _IP = '127.0.0.1'
    _PORT = 8192
    _Socket: socket

    def __init__(self, server_ip: str, server_port: int, queue: Queue, converter: InstructionConverter):
        super().__init__(queue, Token(), converter)

        self._Socket = None

        if server_ip is not None:
            self._IP = server_ip
        if server_port is not None:
            self._PORT = server_port

        self._Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        try:
            self._Socket.connect((self._IP, self._PORT))
        except:
            logger.error(f'connect error')
            return False

        logger.info(f'connect to {(self._IP, self._PORT)}')
        threading.Thread(target=self.start_recv).start()
        return True

    def start_recv(self):
        while self._Token.Status():
            try:
                receive_data = self._Socket.recv(1024)

                if receive_data is None or receive_data == b'':
                    self.close()

                instruction = receive_data.decode("utf-8").strip()

                action = self._Converter.get_action(instruction)

                if action == 'heartbeat':
                    self.send_heartbeat(instruction)
                elif action == 'exit':
                    self.close()
                else:
                    self._Queue.put(instruction)

            except OSError as ex:
                logger.info('net closed...')
                logger.exception(ex)
                self.close()
            except CustomException as ex:
                logger.exception(ex)
                self.send(f'ERROR: {ex.get_code()}')
            except Exception as ex:
                logger.error(ex)
                self.send('ERROR')
        pass

    def send(self, message: str):
        data = message.encode('utf-8')
        if self._Token.Status():
            self._Socket.sendall(data)

    def reply(self, cmd_id, status, message: str = None, **kwargs):
        logger.info('reply message, id {}', cmd_id)
        self.send(self._Converter.reply(cmd_id, status, message, **kwargs))

    def send_heartbeat(self, instruction: str):
        self.send(instruction)

    def is_connected(self):
        return self._Token.Status()

    def close(self):
        self._Queue.put(self._Converter.exit())
        self._Token.Cancel()
        self._Socket.close()
        self._Socket.close()
