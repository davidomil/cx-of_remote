import asyncio
import socket
from abc import ABC, abstractmethod


class Connection(ABC):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket: socket.socket = self.get_socket()
        self.is_connected = False

    @abstractmethod
    def get_socket(self):
        pass

    async def _connect(self):
        self.socket.connect((self.ip, self.port))

    def send(self, data: bytearray):
        self.socket.send(data)

    def read(self):
        raise NotImplementedError()

    async def connect(self):
        while not self.is_connected:
            try:
                # print(f"Connecting to {self.ip} on {self.port}")
                await self._connect()
                # print(f"Connected to {self.ip} on {self.port}")
                self.is_connected = True
            except Exception as e:
                # print(f"Connection to {self.ip} on {self.port} failed with: {str(e)}")
                await asyncio.sleep(1)


class Tcp(Connection):
    def __init__(self, ip, port):
        super().__init__(ip, port)
        self.reader = None
        self.writer = None

    def get_socket(self):
        return asyncio.open_connection(self.ip, self.port)

    async def _connect(self):
        self.reader, self.writer = await asyncio.open_connection(self.ip, self.port)

    def send(self, data: bytearray):
        self.writer.write(data)

    def read(self):
        raise NotImplementedError()


class Udp(Connection):
    def __init__(self, ip, port):
        super().__init__(ip, port)

    def get_socket(self):
        return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
