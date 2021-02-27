# cython: language_level = 3

from libcpp.string cimport string
from libcpp.vector cimport vector
from libcpp.pair cimport pair
from libc.stdint cimport uint64_t, uint32_t

cdef extern from "ripemd.hpp":
    pair[string, vector[uint32_t]] ripemd320_with_bit_change(string message, uint64_t bit_pos)
    string ripemd320(string message)
