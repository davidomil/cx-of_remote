HAND_SHAKE = bytearray([0xcc, 0x80, 0x80, 0x80, 0x80, 0x00, 0x00, 0x00, 0x00, 0x33
                        ])

SECOND_HANDSHAKE = bytearray(b"\x63\x63\x01\x00\x00\x00\x00")

DATA_HEAD = bytearray(b"\x63\x63\x0a\x00\x00\x0a\x00")
SOME_DATA = bytearray(b"\xcc\x80\x80\x80\x80\x00\x00\x00")

FLY_UP = bytearray(b"\xcc\x80\x80\x80\x80\x01\x00\x00")
LAND = bytearray(b"\xcc\x80\x80\x80\x80\x00\x00\x00")
