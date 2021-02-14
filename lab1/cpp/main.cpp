#include "ripemd.hpp"

int main()
{
    // "examples" - b8fa78c68ca04ca41a0cfb9d2491424ca057412905df03b6c312a6dd3eacc3b5a76b603e45fe0180
    RIPEMD_320 hash;
    hash.read_message("examples");
    cout << hash.ripemd_320();
    return 0;
}