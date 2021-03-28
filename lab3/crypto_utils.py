from Cryptodome.Cipher import DES3, DES, AES, Blowfish, PKCS1_OAEP
from Cryptodome.Signature import pss
from Cryptodome.PublicKey import RSA
from Cryptodome.Hash import SHA256, MD5, RIPEMD160
from Cryptodome.Util.Padding import pad, unpad


DES_KEYS_LENGTHS = [8, 16, 24]
AES_KEYS_LENGTHS = [16, 24, 32]


def handle_symmetric_by_mode(symmetric, data, mode):
    if mode == 'encrypt':
        return symmetric.encrypt(pad(data, symmetric.block_size))
    elif mode == 'decrypt':
        return unpad(symmetric.decrypt(data), symmetric.block_size)
    else:
        raise ValueError(f'crypto_utils.symmetric_by_mode: Unable to handle mode: {mode}')


def handle_des(data: bytes, key: bytes, mode='encrypt'):
    if len(key) not in DES_KEYS_LENGTHS:
        return

    if len(key) == 8:
        des = DES.new(key, DES.MODE_ECB)

    if len(key) in [16, 24]:
        key = DES3.adjust_key_parity(key)
        des = DES3.new(key, DES3.MODE_ECB)

    return handle_symmetric_by_mode(des, data, mode)


def handle_aes(data: bytes, key: bytes, mode='encrypt'):
    if len(key) not in AES_KEYS_LENGTHS:
        return

    aes = AES.new(key, AES.MODE_ECB)
    return handle_symmetric_by_mode(aes, data, mode)


def handle_blowfish(data: bytes, key: bytes, mode='encrypt'):
    if not (5 <= len(key) <= 56):
        return

    blowfish = Blowfish.new(key, Blowfish.MODE_ECB)
    return handle_symmetric_by_mode(blowfish, data, mode)


def handle_pkcs1_oaep(data: bytes, key: bytes, mode='encrypt'):
    rsa_key = RSA.importKey(key)
    pkcs1 = PKCS1_OAEP.new(rsa_key)
    return getattr(pkcs1, mode)(data)


def signature_pss(data: bytes, key: bytes):
    rsa_key = RSA.importKey(key)
    sha_hash = SHA256.new(data)

    return pss.new(rsa_key).sign(sha_hash)


def verify_signature_pss(data: bytes, key: bytes, signature: bytes):
    rsa_key = RSA.importKey(key)
    sha_hash = SHA256.new(data)

    pss.new(rsa_key).verify(sha_hash, signature)


def hash_sha256(data: bytes):
    sha = SHA256.new()
    sha.update(data)
    return sha.hexdigest()


def hash_md5(data: bytes):
    md5 = MD5.new()
    md5.update(data)
    return md5.hexdigest()


def hash_ripemd160(data: bytes):
    ripemd160 = RIPEMD160.new()
    ripemd160.update(data)
    return ripemd160.hexdigest()
