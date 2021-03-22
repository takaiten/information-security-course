from Cryptodome.Cipher import DES3, DES, AES, Blowfish, PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from Cryptodome.Hash import SHA256, MD5, RIPEMD160


DES_KEYS_LENGTHS = [8, 16, 24]
AES_KEYS_LENGTHS = [16, 24, 32]


def handle_des(data: bytes, key: bytes, mode='encrypt'):
    if len(key) not in DES_KEYS_LENGTHS:
        return

    if len(key) == 8:
        des = DES.new(key, DES.MODE_OPENPGP)

    if len(key) in [16, 24]:
        key = DES3.adjust_key_parity(key)
        des = DES3.new(key, DES3.MODE_OPENPGP)

    return getattr(des, mode)(data)


def handle_aes(data: bytes, key: bytes, mode='encrypt'):
    if len(key) not in AES_KEYS_LENGTHS:
        return

    aes = AES.new(key, AES.MODE_OPENPGP)
    return getattr(aes, mode)(data)


def handle_blowfish(data: bytes, key: bytes, mode='encrypt'):
    if not (5 <= len(key) <= 56):
        return

    blowfish = Blowfish.new(key, Blowfish.MODE_OPENPGP)
    return getattr(blowfish, mode)(data)


def handle_pkcs1(data: bytes, key: bytes, mode='encrypt'):
    rsa_key = RSA.importKey(key)
    pkcs1 = PKCS1_OAEP.new(rsa_key)
    return getattr(pkcs1, mode)(data)


def sha256_hash(data: bytes):
    sha = SHA256.new()
    sha.update(data)
    return sha.hexdigest()


def md5_hash(data: bytes):
    md5 = MD5.new()
    md5.update(data)
    return md5.hexdigest()


def ripemd160_hash(data: bytes):
    ripemd160 = RIPEMD160.new()
    ripemd160.update(data)
    return ripemd160.hexdigest()
