import asyncio

from configuration import *
from tcp import Tcp, Udp

IP = '192.168.0.1'
TCP_PORT1 = 7060
TCP_PORT2 = 8060

UDP_PORT1 = 50000
UDP_PORT2 = 40000


class DroneControl:
    def __init__(self):
        self.tcp_connection = Tcp(IP, TCP_PORT1)
        self.tcp_connection2 = Tcp(IP, TCP_PORT2)
        self.udp_connection = Udp(IP, UDP_PORT1)
        self.udp_connection2 = Udp(IP, UDP_PORT2)
        self.data = SOME_DATA
        pass

    def reset_data(self):
        self.data = SOME_DATA

    def disconnect(self):
        pass

    async def loop(self):
        asyncio.create_task(self.tcp_connection.connect())
        asyncio.create_task(self.tcp_connection2.connect())

        await asyncio.gather(self.udp_connection.connect(), self.udp_connection2.connect())

        asyncio.create_task(self.keep_sending_data(self.udp_connection, HAND_SHAKE))


        handshake = False
        while True:
            if not handshake:
                try:
                    print(f"Sending Handshake to {self.udp_connection.ip}:{self.udp_connection.port}")
                    self.udp_connection2.send(SECOND_HANDSHAKE)
                    handshake = True
                    print("Handshake succeeded")
                except ConnectionRefusedError:
                    print("Sending Handshake failed")

            try:
                # print(SOME_DATA_test)
                # print(self.make_packet(SOME_DATA))
                self.udp_connection2.send(self.make_packet(self.data))
            except ConnectionRefusedError:
                print("Sending data failed")
            await asyncio.sleep(0.05)

    def checksum(self, data):
        return_data = (data[1] ^ data[2] ^ data[3] ^ data[4] ^ data[5]) & 0xFF
        return return_data

    def make_packet(self, data):
        data = DATA_HEAD + data + bytearray(bytes([self.checksum(data[:])])) + bytearray(b'\x33')
        # print(data)
        return data

    async def keep_sending_data(self, connection, data):
        while True:
            try:
                connection.send(data)
            except ConnectionRefusedError:
                pass
            finally:
                await asyncio.sleep(1)
