# distutils: language = c++
# distutils: sources = ../cpp/ripemd.cpp ../cpp/helpers.cpp
from libcpp.string cimport string

cdef extern from "../cpp/ripemd.hpp":
    string ripemd320(string message)


def py_ripemd320(message: str) -> str:
    cdef string msg_str = message.encode('ascii')
    cdef string hash_res = ripemd320(msg_str)
    cdef str hash_str = hash_res.decode('ascii')

    return hash_str
