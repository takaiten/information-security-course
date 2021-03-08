from sys import byteorder
from time import time
from struct import unpack
from itertools import islice
from Cryptodome.Cipher import DES3
from Cryptodome.Util.strxor import strxor
from typing import List


def str_to_bytes(s: str) -> bytes:
    return s.encode('UTF-8')


def get_8_byte_time() -> bytes:
    t = int(time() * 10 ** 6)
    return str_to_bytes(hex(t)[-8:])


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


def convert_to_dec_and_bin(sequence: List[bytes]) -> (str, str):
    sequence_str_dec = ''
    sequence_str_bin = ''

    for item in sequence:
        # 'Q' means unsigned long long in C (8 bytes)
        sequence_str_dec += str(unpack('Q', item)[0])
        # slice to remove '0b'
        sequence_str_bin += bin(int.from_bytes(item, byteorder=byteorder))[2:]

    return sequence_str_bin, sequence_str_dec
