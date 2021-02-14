#include <cstring>
#include "ripemd.hpp"

//#include <bits/stdc++.h>
//
//void strToBinary(string s)
//{
//    int n = s.length();
//
//
//    for (int i = 0; i <= n; i++)
//    {
//        // convert each char to
//        // ASCII value
//        int val = int(s[i]);
//
//        // Convert ASCII value to binary
//        string bin = "";
//        while (val > 0)
//        {
//            (val % 2)? bin.push_back('1') :
//            bin.push_back('0');
//            val /= 2;
//        }
//        reverse(bin.begin(), bin.end());
//
//        cout << bin << " ";
//    }
//}

uint32_t RIPEMD::Helpers::f(const uint8_t j, uint16_t x, uint16_t y, uint16_t z) {
    switch (j) {
        case 0 ... 15:
            return x ^ y ^ z;
        case 16 ... 31:
            return (x & y) | (~x & z);
        case 32 ... 47:
            return (x | ~y) ^ z;
        case 48 ... 63:
            return (x & z) | (y & ~z);
        case 64 ... 79:
            return x ^ (y | ~z);
        default:
            throw invalid_argument("Helpers::f: j must be in range from 0 to 70");
    }
}

uint16_t RIPEMD::Helpers::K1(const uint8_t j) {
    switch (j) {
        case 0 ... 15:
            return 0;
        case 16 ... 31:
            return (uint16_t)0x5a827999;
        case 32 ... 47:
            return (uint16_t)0x6ed9eba1;
        case 48 ... 63:
            return (uint16_t)0x8f1bbcdc;
        case 64 ... 79:
            return (uint16_t)0xa953fd4e;
        default:
            throw invalid_argument("Helpers::K1: j must be in range from 0 to 70");
    }
}

uint16_t RIPEMD::Helpers::K2(const uint8_t j) {
    switch (j) {
        case 0 ... 15:
            return (uint16_t)0x50a28be6;
        case 16 ... 31:
            return (uint16_t)0x5c4dd124;
        case 32 ... 47:
            return (uint16_t)0x6d703ef3;
        case 48 ... 63:
            return (uint16_t)0x7a6d76e9;
        case 64 ... 79:
            return 0;
        default:
            throw invalid_argument("Helpers::K2: j must be in range from 0 to 70");
    }
}

void RIPEMD::RIPEMD320::append_additional_bits() {
//    msg += '1';
//
//    while (msg.length() % 512 != 448) {
//        msg += '0';
//    }
}

void RIPEMD::RIPEMD320::append_msg_length_bits() {
//    bitset<64> length_bitset(initial_length);
//    string bitset_string = length_bitset.to_string();
//
//    msg.append(bitset_string.substr(32, 32));
//    msg.append(bitset_string.substr(0, 32));
}

void RIPEMD::RIPEMD320::hash(const uint8_t* msg, uint32_t msg_len) {
//    int j;
//    for (uint32_t i = 0; i < (msg_len >> 6); ++i) {
//        uint32_t chunk[16];
//
//        for (j = 0; j < 16; ++j) {
//            chunk[j] = (uint32_t)(*(msg++));
//            chunk[j] |= (uint32_t)(*(msg++)) << 8;
//            chunk[j] |= (uint32_t)(*(msg++)) << 16;
//            chunk[j] |= (uint32_t)(*(msg++)) << 24;
//        }
//
//        compress(digest, chunk);
//    }
    uint32_t chunk[16] = {0};

    for (uint32_t i = 0; i < (msg_len & 63); ++i) {
        chunk[i >> 2] ^= (uint32_t)*msg++ << ((i & 3) << 3);
    }

    chunk[(msg_len >> 2) & 15] ^= (uint32_t)1 << (8 * (msg_len & 3) + 7);

    // 55 - because 56 * 8 = 448 which is left border of the chunk
    if ((msg_len & 63) > 55) {
//        compress(digest, chunk);
        memset(chunk, 0, 64);
    }

    chunk[14] = msg_len << 3;
    chunk[15] = (msg_len >> 29);
}

RIPEMD::RIPEMD320::RIPEMD320() {

}
