from Cryptodome.Hash import SHA256
from random import choice

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
DEFAULT_SALT_SIZE = 10


def hash_sha256(data: str):
    data_bytes = data.encode('UTF-8')

    sha = SHA256.new()
    sha.update(data_bytes)
    return sha.hexdigest()


def generate_salt(size: int = DEFAULT_SALT_SIZE):
    salt = []
    for i in range(size):
        salt.append(choice(ALPHABET))

    return "".join(salt)


def hash_password(password: str, salt: str):
    return hash_sha256(password + salt)
