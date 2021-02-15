#include "helpers.hpp"

// Нелинейная побитовая функция F
uint32_t F(uint32_t j, uint32_t x, uint32_t y, uint32_t z) {
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
            return 0x00000000;
    }
}

// Добавляемые 16-ичные константы
uint32_t K1(uint32_t j) {
    switch (j) {
        case 0 ... 15:
            return 0x00000000;
        case 16 ... 31:
            return 0x5A827999;
        case 32 ... 47:
            return 0x6ED9EBA1;
        case 48 ... 63:
            return 0x8F1BBCDC;
        case 64 ... 79:
            return 0xA953FD4E;
        default:
            return 0x00000000;
    }
}

// Добавляемые 16-ичные константы
uint32_t K2(uint32_t j) {
    switch (j) {
        case 0 ... 15:
            return 0x50A28BE6;
        case 16 ... 31:
            return 0x5C4DD124;
        case 32 ... 47:
            return 0x6D703EF3;
        case 48 ... 63:
            return 0x7A6D76E9;
        case 64 ... 79:
            return 0x00000000;
        default:
            return 0x00000000;
    }
}

// Смена порядка бит
uint32_t inv(uint32_t value) {
    uint32_t res = 0;

    res |= ((value >> 0) & 0xFF) << 24;
    res |= ((value >> 8) & 0xFF) << 16;
    res |= ((value >> 16) & 0xFF) << 8;
    res |= ((value >> 24) & 0xFF) << 0;

    return res;
}

// Преобразование 4-х байт в uint32_t
uint32_t bytes_to_uint(const char *bytes) {
    uint32_t res = 0;

    res |= ((uint32_t) bytes[3] << 24) & 0xFF000000;
    res |= ((uint32_t) bytes[2] << 16) & 0xFF0000;
    res |= ((uint32_t) bytes[1] << 8) & 0xFF00;
    res |= ((uint32_t) bytes[0] << 0) & 0xFF;

    return res;
}
