cmake_minimum_required(VERSION 3.17)
project(hashpkg)

set(CMAKE_CXX_STANDARD 20)

add_executable(hashpkg main.cpp const.hpp helpers.hpp helpers.cpp ripemd.hpp ripemd.cpp)
