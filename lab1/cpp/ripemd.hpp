#include <cmath>
#include <string>
#include <utility>
#include <stdexcept>

namespace RIPEMD {
    using std::string, std::invalid_argument;

    namespace Helpers {
        static uint32_t f(uint8_t j, uint16_t x, uint16_t y, uint16_t z);
        static uint16_t K1(uint8_t j);
        static uint16_t K2(uint8_t j);
    }

    class RIPEMD320 {
    private:
//        string msg;
//        size_t bit_len;
    protected:
        void append_additional_bits();
        void append_msg_length_bits();
    public:
        // TODO: convert message to binary representation
        explicit RIPEMD320();
        void hash(const uint8_t* msg, uint32_t msg_len);
    };
};
