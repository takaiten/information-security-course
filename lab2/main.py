from time import time
from Cryptodome.Cipher import DES3
from Cryptodome.Util.strxor import strxor


def str_to_bytes(s: str) -> bytes:
    return s.encode('UTF-8')


def get_8_byte_time() -> bytes:
    t = int(time() * 10 ** 6)
    return str_to_bytes(hex(t)[-8:])


def ansi_x9_17(key1: str, key2: str, seed: str):
    des3 = DES3.new(str_to_bytes(key1 + key2), DES3.MODE_ECB)
    temp = des3.encrypt(get_8_byte_time())
    s = str_to_bytes(seed)

    while True:
        x = des3.encrypt(strxor(s, temp))
        s = des3.encrypt(strxor(x, temp))
        yield x


def main():
    key1 = '12345678'
    key2 = '87654321'
    seed = 'examples'
    m = 2

    sequence = [x for x, i in zip(ansi_x9_17(key1, key2, seed), range(m))]
    print(sequence)


if __name__ == '__main__':
    main()
