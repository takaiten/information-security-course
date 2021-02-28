# distutils: language = c++
# distutils: sources = ripemd.cpp helpers.cpp

from ripemd320 cimport ripemd320_with_bit_change, ripemd320

# Create python function definitions for cython code
def py_ripemd320_with_shift(message: str, bit_pos: int) -> tuple:
    cdef string msg_str = message.encode('ascii')

    cdef pair[string, vector[uint32_t]] res = ripemd320_with_bit_change(msg_str, bit_pos)

    return res.first.decode('ascii'), res.second

def py_ripemd320(message: str) -> str:
    cdef string msg_str = message.encode('ascii')

    cdef pair[string, vector[uint32_t]] res = ripemd320(msg_str)

    return res.first.decode('ascii'), res.second
