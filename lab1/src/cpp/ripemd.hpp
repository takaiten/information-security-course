#include <string>

namespace methods {
    void add_additional_bits(std::string &message);
    uint32_t **generate_blocks_array(uint32_t blocks_count, uint64_t bitlen, std::string &message);
    uint32_t *generate_hashes(uint32_t blocks_count, uint32_t **blocks);
    void change_bit(uint32_t **blocks, uint64_t  bit_pos);
}

std::string ripemd320(std::string message);
std::string ripemd320_with_bit_change(std::string message, uint64_t bit_pos);
