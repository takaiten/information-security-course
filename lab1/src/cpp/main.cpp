#include "ripemd.hpp"
#include <iostream>

int main() {
    auto result = ripemd320_with_bit_change("examples", 2);

    std::cout << result.first;

    return 0;
}
