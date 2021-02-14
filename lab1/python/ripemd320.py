# ===========
# HELPERS
# ===========
def rotl(value, bits):
    return (value << bits) | (value >> (32 - bits))


def rotr(value, bits):
    return (value >> bits) | (value << (32 - bits))


def logical_xor(str1, str2):
    return bool(str1) ^ bool(str2)

# ===========
# RIPEMD implementation
# ===========

def string_to_int(string=''):
    return int(string.encode('utf-8').hex(), 16)


def ripemd320(message):
    byte_msg = string_to_int(message)
    a=0

def main():
    message = "a"
    result = ripemd320(message)

if __name__ == "__main__":
    main()