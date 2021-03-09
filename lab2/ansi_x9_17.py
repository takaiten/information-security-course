from time import time_ns
from typing import List
from itertools import islice
from Cryptodome.Cipher import DES3, DES
from Cryptodome.Util.strxor import strxor


def str_to_bytes(s: str) -> bytes:
    return s.encode('ascii')


def get_8_byte_time() -> bytes:
    t = hex(time_ns())
    return str_to_bytes(t[-8:])


def ansi_x9_17(key: bytes, s: bytes) -> bytes:
    des3 = DES3.new(key, DES3.MODE_ECB)
    temp = des3.encrypt(get_8_byte_time())

    while True:
        x = des3.encrypt(strxor(s, temp))
        s = des3.encrypt(strxor(x, temp))
        yield x


def generate_sequence(key1: str, key2: str, seed: str, m: int) -> List[bytes]:
    key = str_to_bytes(key1 + key2)
    s = str_to_bytes(seed)

    return [x for x in islice(ansi_x9_17(key, s), m)]


def convert_to_bin_and_hex(sequence: List[bytes]) -> (str, str):
    sequence_str_bin = ''
    sequence_str_hex = ''

    for block in sequence:
        h = block.hex()
        sequence_str_hex += h
        # slice to remove '0b'
        sequence_str_bin += bin(int(h, 16))[2:].zfill(64)

    return sequence_str_bin, sequence_str_hex
