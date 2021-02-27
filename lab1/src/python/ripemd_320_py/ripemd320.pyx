# distutils: language = c++
# distutils: sources = ../../cpp/ripemd.cpp ../../cpp/helpers.cpp
# cython: language_level=3
from libcpp.string cimport string
from libcpp.vector cimport vector
from libcpp.pair cimport pair
from libc.stdint cimport uint64_t, uint32_t


cdef extern from "../../cpp/ripemd.hpp":
    pair[string, vector[uint32_t]] ripemd320_with_bit_change(string message, uint64_t bit_pos)
    string ripemd320(string message)


def py_ripemd320(message: str, bit_pos: int) -> tuple:
    cdef string msg_str = message.encode('ascii')

    cdef pair[string, vector[uint32_t]] res = ripemd320_with_bit_change(msg_str, bit_pos)

    return res.first.decode('ascii'), res.second


def py_ripemd320__(message: str) -> str:
    cdef string msg_str = message.encode('ascii')
    return ripemd320(msg_str).decode('ascii')
