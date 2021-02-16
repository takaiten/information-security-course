# distutils: language = c++
# distutils: sources = ../cpp/ripemd.cpp ../cpp/helpers.cpp
from libcpp.string cimport string
from libc.stdint cimport uint64_t

cdef extern from "../cpp/ripemd.hpp":
    string ripemd320_with_bit_change(string message, uint64_t bit_pos)
    string ripemd320(string message)


def py_ripemd320(message: str, bit_pos: int=None) -> str:
    cdef string msg_str = message.encode('ascii')
    cdef string hash_res = ripemd320(msg_str) if bit_pos is None else ripemd320_with_bit_change(msg_str, bit_pos)
    cdef str hash_str = hash_res.decode('ascii')

    return hash_str
