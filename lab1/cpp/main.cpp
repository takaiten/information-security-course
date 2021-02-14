#include "ripemd.hpp"

int main()
{
    RIPEMD_320 hash;
    hash.read_message("");
    cout << hash.ripemd_320();
    return 0;
}