def encode_utf8(data: str):
    return data.encode('UTF-8')


def decode_utf8(data: bytes):
    return data.decode('UTF-8')


def bytes_to_hex(data: bytes):
    return data.hex()


def bytes_from_hex(data: str):
    return bytes.fromhex(data)