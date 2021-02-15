#include "ripemd.hpp"

using namespace RIPEMD;

int main()
{
    // "examples" - b8fa78c68ca04ca41a0cfb9d2491424ca057412905df03b6c312a6dd3eacc3b5a76b603e45fe0180
    string msg = "examples";
    cout << "Message: " << msg << "\nHash: " << RIPEMD_320::ripemd_320(msg);
    return 0;
}