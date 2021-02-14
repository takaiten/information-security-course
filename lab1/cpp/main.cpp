#include <iostream>

#include "ripemd.hpp"

using namespace RIPEMD;

int main() {
    auto *md = new RIPEMD320();
    md->hash((uint8_t*)("abc"), 3);

    return 0;
}
